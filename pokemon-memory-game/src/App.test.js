import React from "react";
import {
  render,
  screen,
  fireEvent,
  act,
  waitFor,
} from "@testing-library/react";
import "@testing-library/jest-dom";
import App, { pokemons } from "./App";

describe("App Component", () => {
  beforeEach(() => {
    jest.useFakeTimers();
  });

  afterEach(() => {
    jest.clearAllMocks();
    jest.useRealTimers();
  });

  test("renders without crashing", () => {
    render(<App />);
    expect(screen.getByText(/moves/i)).toBeInTheDocument();
  });

  test("displays the correct number of pokemon cards", () => {
    render(<App />);
    const pokemonCards = screen.getAllByRole("button", {
      name: /pokemon-card/i,
    });
    expect(pokemonCards.length).toBe(12);
  });

  test("increments move count when a card is clicked", () => {
    render(<App />);
    const card = screen.getAllByRole("button", {
      name: "pokemon-card-charizard",
    })[0];
    fireEvent.click(card);
    const movesElement = screen.getByTestId("moves-count");
    expect(movesElement.textContent).toBe("1 moves");
  });

  test("increments correctly with each unique card click", async () => {
    render(<App />);

    const movesElement = screen.getByTestId("moves-count");
    expect(movesElement.textContent).toBe("0 moves");

    const cards = screen.getAllByRole("button", {
      name: /^pokemon-card/i,
    });

    fireEvent.click(cards[0]);
    await waitFor(() => expect(movesElement.textContent).toBe("1 moves"));

    fireEvent.click(cards[1]);
    await waitFor(() => expect(movesElement.textContent).toBe("2 moves"));

    fireEvent.click(cards[0]);
    await waitFor(() => expect(movesElement.textContent).toBe("2 moves"));

    fireEvent.click(cards[2]);
    await waitFor(() => expect(movesElement.textContent).toBe("3 moves"));
  });

  test("cards match when two of the same pokemon are selected", () => {
    render(<App />);
    const firstCharizardCard = screen.getAllByRole("button", {
      name: "pokemon-card-charizard",
    })[0];
    fireEvent.click(firstCharizardCard);

    const secondCharizardCard = screen.getAllByRole("button", {
      name: "pokemon-card-charizard",
    })[1];
    fireEvent.click(secondCharizardCard);

    expect(firstCharizardCard).toHaveClass("flipped");
    expect(secondCharizardCard).toHaveClass("flipped");
  });

  test("flips back two cards when they don't match", () => {
    render(<App />);

    const cards = screen.getAllByRole("button", {
      name: /^pokemon-card/i,
    });

    fireEvent.click(cards[0]);
    fireEvent.click(cards[1]);

    expect(cards[0]).toHaveClass("flipped");
    expect(cards[1]).toHaveClass("flipped");

    act(() => {
      jest.runAllTimers();
    });

    expect(cards[0]).not.toHaveClass("flipped");
    expect(cards[1]).not.toHaveClass("flipped");
  });

  test("shows win alert when all cards are matched", async () => {
    const alertMock = jest.spyOn(window, 'alert').mockImplementation(() => {});
    render(<App />);
    
    // Match all pairs of cards
    const cards = screen.getAllByRole("button", { name: /^pokemon-card/i });
    for (let i = 0; i < pokemons.length; i++) {
      const cardName = pokemons[i].name;
      const matchingCards = screen.getAllByRole("button", {
        name: `pokemon-card-${cardName}`,
      });
      
      fireEvent.click(matchingCards[0]);
      fireEvent.click(matchingCards[1]);
      
      act(() => {
        jest.runAllTimers();
      });
    }

    expect(alertMock).toHaveBeenCalledWith("You won!");
    alertMock.mockRestore();
  });

  test("prevents clicking more than two cards at once", () => {
    render(<App />);
    const cards = screen.getAllByRole("button", { name: /^pokemon-card/i });
    
    // Click three cards in succession
    fireEvent.click(cards[0]);
    fireEvent.click(cards[1]);
    fireEvent.click(cards[2]);
    
    // Only the first two cards should be flipped
    expect(cards[0]).toHaveClass("flipped");
    expect(cards[1]).toHaveClass("flipped");
    expect(cards[2]).not.toHaveClass("flipped");
  });

  test("prevents clicking already matched cards", async () => {
    render(<App />);
    
    // Find and match a pair of cards
    const firstPairCards = screen.getAllByRole("button", {
      name: `pokemon-card-${pokemons[0].name}`,
    });
    
    fireEvent.click(firstPairCards[0]);
    fireEvent.click(firstPairCards[1]);
    
    act(() => {
      jest.runAllTimers();
    });
    
    // Try clicking the matched cards again
    fireEvent.click(firstPairCards[0]);
    fireEvent.click(firstPairCards[1]);
    
    // Move count should still be 1 (from the initial match)
    const movesElement = screen.getByTestId("moves-count");
    expect(movesElement.textContent).toBe("1 moves");
  });

  test("displays correct Pokemon images when cards are flipped", () => {
    render(<App />);
    const firstCard = screen.getAllByRole("button", {
      name: `pokemon-card-${pokemons[0].name}`,
    })[0];
    
    fireEvent.click(firstCard);
    
    const pokemonImage = firstCard.querySelector("img");
    expect(pokemonImage).toHaveAttribute(
      "src",
      `https://assets.pokemon.com/assets/cms2/img/pokedex/full/${pokemons[0].id}.png`
    );
    expect(pokemonImage).toHaveAttribute("alt", pokemons[0].name);
  });
});

import React, { useState, useEffect } from "react";
import shuffle from "lodash.shuffle";
import "./App.css";

// Pokemon data
export const pokemons = [
  { id: "004", name: "charizard" },
  { id: "010", name: "caterpie" },
  { id: "077", name: "ponyta" },
  { id: "108", name: "lickitung" },
  { id: "132", name: "ditto" },
  { id: "133", name: "eevee" },
];

const doublePokemon = shuffle([...pokemons, ...pokemons]);

export default function App() {
  const [flippedCardsIndexes, setFlippedCardsIndexes] = useState([]);
  const [matchedCards, setMatchedCards] = useState([]);
  const [moves, setMoves] = useState(0);
  const [isChecking, setIsChecking] = useState(false);

  // Handle card matching logic
  useEffect(() => {
    if (flippedCardsIndexes.length === 2) {
      setIsChecking(true);
      const [firstIndex, secondIndex] = flippedCardsIndexes;
      const firstCard = doublePokemon[firstIndex];
      const secondCard = doublePokemon[secondIndex];

      if (firstCard.name === secondCard.name) {
        // Match successful: update matched cards
        setMatchedCards(prev => {
          const newMatchedCards = [...prev, firstIndex, secondIndex];
          // If this is the last pair of matched cards, show victory message after a short delay
          if (newMatchedCards.length === doublePokemon.length) {
            setTimeout(() => {
              alert("You won!");
            }, 500); // Allow enough time for the last card flip animation to complete
          }
          return newMatchedCards;
        });
        // Clear flipped cards
        setFlippedCardsIndexes([]);
        setIsChecking(false);
      } else {
        // Match failed: flip cards back after delay
        setTimeout(() => {
          setFlippedCardsIndexes([]);
          setIsChecking(false);
        }, 1000);
      }
    }
  }, [flippedCardsIndexes]);

  function flipCard(index) {
    // If currently checking for a match, return
    if (isChecking) {
      return;
    }

    // If card is already matched, return
    if (matchedCards.includes(index)) {
      return;
    }

    // If card is already flipped, return
    if (flippedCardsIndexes.includes(index)) {
      return;
    }

    // If two cards are already flipped, return
    if (flippedCardsIndexes.length === 2) {
      return;
    }

    // Increment move count (only for valid card flips)
    setMoves(prev => prev + 1);

    // Update flipped cards
    setFlippedCardsIndexes(prev => [...prev, index]);
  }

  return (
    <div className="app">
      <h1>Pokémon Memory Game</h1>
      <p data-testid="moves-count">
        {moves} <strong>moves</strong>
      </p>

      <div className="cards">
        {doublePokemon.map((pokemon, index) => {
          const isFlipped = flippedCardsIndexes.includes(index) || matchedCards.includes(index);
          const isMatched = matchedCards.includes(index);

          return (
            <PokemonCard
              key={index}
              index={index}
              pokemon={pokemon}
              isFlipped={isFlipped}
              isMatched={isMatched}
              flipCard={flipCard}
            />
          );
        })}
      </div>
    </div>
  );
}

// Individual Pokemon card component
export function PokemonCard({ index, pokemon, isFlipped, isMatched, flipCard }) {
  return (
    <button
      className={`pokemon-card ${isFlipped ? "flipped" : ""}`}
      onClick={() => flipCard(index)}
      aria-label={`pokemon-card-${pokemon.name}`}
      disabled={isFlipped || isMatched}
    >
      <div className="inner">
        <div className="front">
          <img
            src={`https://assets.pokemon.com/assets/cms2/img/pokedex/full/${pokemon.id}.png`}
            alt={pokemon.name}
            width="100"
          />
        </div>
        <div className="back">?</div>
      </div>
    </button>
  );
}

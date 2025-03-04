import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import App from "./App";

test("renders the App with initial state", () => {
  render(<App />);
  expect(screen.getByText("Northeastern University (0)")).toBeInTheDocument();
});

test("renders header counter and updates on item addition", async () => {
  render(<App />);

  const addButton = screen.getByLabelText("Add James Carmona");
  userEvent.click(addButton);

  await waitFor(() => {
    expect(screen.getByText("Northeastern University (1)")).toBeInTheDocument();
  });

  const secondAddButton = screen.getByLabelText("Add Leslie Abbott");
  userEvent.click(secondAddButton);

  await waitFor(() => {
    expect(screen.getByText("Northeastern University (2)")).toBeInTheDocument();
  });
});

test("select multiple items and then delete them", async () => {
  render(<App />);

  const addButtonForItem1 = screen.getByRole("button", {
    name: "Add Hector Adams",
  });
  userEvent.click(addButtonForItem1);

  await waitFor(() => {
    expect(screen.getByText("Hector Adams")).toBeInTheDocument();
  });

  const selectedItems1 = screen.queryAllByRole("listitem", {
    name: /selected-/,
  });
  expect(selectedItems1).toHaveLength(1);

  const deleteButtonForItem1 = screen.getByRole("button", {
    name: `Delete Hector Adams`,
  });
  userEvent.click(deleteButtonForItem1);

  await waitFor(() => {
    expect(screen.getByText("Hector Adams")).toBeInTheDocument();
  });

  const selectedItems2 = screen.queryAllByRole("listitem", {
    name: /selected-/,
  });
  expect(selectedItems2).toHaveLength(0);
});

test("selects all items when 'Add All' button is clicked", async () => {
  render(<App />);

  expect(screen.getByText("Northeastern University (0)")).toBeInTheDocument();

  const addAllButton = screen.getByRole("button", { name: "Add All" });
  userEvent.click(addAllButton);

  await waitFor(() => {
    expect(
      screen.getByText("Northeastern University (10)")
    ).toBeInTheDocument();
  });
});

test("[Optional] search functionality filters the item list", async () => {
  render(<App />);

  const searchInput = screen.getByPlaceholderText(
    "Search by name or department"
  );
  userEvent.type(searchInput, "James Carmona");

  await waitFor(() => {
    const displayedItem = screen.getByLabelText("item-James Carmona");
    expect(displayedItem).toBeInTheDocument();
  });

  const allDisplayedItems = screen.getAllByRole("listitem");
  expect(allDisplayedItems.length).toBe(1);
});

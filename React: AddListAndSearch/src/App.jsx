import { useState, useEffect } from "react";
import Header from "./components/Header";
import ItemPicker from "./components/ItemPicker";
import ItemsSelected from "./components/ItemsSelected";
import "./App.css";

// Initial state containing all available items with their details
const itemsInitialState = [
  {
    id: 1,
    name: "Hector Adams",
    subTitle: "Engineer",
    imageUrl:
      "https://images.unsplash.com/photo-1519345182560-3f2917c472ef?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80",
  },
  {
    id: 2,
    name: "James Carmona",
    subTitle: "Data Science",
    imageUrl:
      "https://images.unsplash.com/photo-1463453091185-61582044d556?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80",
  },
  {
    id: 3,
    name: "Blake Alexander",
    subTitle: "Slytherim",
    imageUrl:
      "https://images.unsplash.com/photo-1502685104226-ee32379fefbe?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80",
  },
  {
    id: 4,
    name: "Leslie Abbott",
    subTitle: "Engineer",
    imageUrl:
      "https://images.unsplash.com/photo-1500917293891-ef795e70e1f6?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80",
  },
  {
    id: 5,
    name: "Yvette Blanchard",
    subTitle: "Slytherim",
    imageUrl:
      "https://images.unsplash.com/photo-1501031170107-cfd33f0cbdcc?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80",
  },
  {
    id: 6,
    name: "Kristin Watson",
    subTitle: "Human Resources",
    imageUrl:
      "https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80",
  },
  {
    id: 7,
    name: "Emily Wilson",
    subTitle: "User Experience",
    imageUrl:
      "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80",
  },
  {
    id: 8,
    name: "Angela Beaver",
    subTitle: "Slytherim",
    imageUrl:
      "https://images.unsplash.com/photo-1520785643438-5bf77931f493?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80",
  },
  {
    id: 9,
    name: "Fabricio Andrews",
    subTitle: "Human Resources",
    imageUrl:
      "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80",
  },
  {
    id: 10,
    name: "Angela Smith",
    subTitle: "User Experience",
    imageUrl:
      "https://images.unsplash.com/photo-1506980595904-70325b7fdd90?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80",
  },
];

function App() {
  // State management for available items, selected items, and search functionality
  const [availableItems, setAvailableItems] = useState(itemsInitialState);
  const [selectedItems, setSelectedItems] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");

  // Handler to add a single item from available to selected list
  const handleAddItem = (item) => {
    setSelectedItems([...selectedItems, item]);
    setAvailableItems(availableItems.filter((i) => i.id !== item.id));
  };

  // Handler to remove a single item from selected list back to available items
  const handleRemoveItem = (item) => {
    setAvailableItems([...availableItems, item]);
    setSelectedItems(selectedItems.filter((i) => i.id !== item.id));
  };

  // Handler to move all available items to selected list
  const handleAddAll = () => {
    setSelectedItems([...selectedItems, ...availableItems]);
    setAvailableItems([]);
  };

  // Handler to update search term for filtering items
  const handleSearch = (term) => {
    setSearchTerm(term);
  };

  // Filter available items based on search term
  // Searches both name and subtitle fields, case-insensitive
  const filteredItems = availableItems.filter((item) => {
    if (!searchTerm) return true;
    const searchLower = searchTerm.toLowerCase();
    return (
      item.name.toLowerCase().includes(searchLower) ||
      item.subTitle.toLowerCase().includes(searchLower)
    );
  });

  // Debug effect to log state changes
  useEffect(() => {
    console.log('Selected items updated:', selectedItems);
  }, [selectedItems]);

  return (
    <div className="item-picker-wrapper p-5 m-5">
      <Header 
        title="Northeastern University" 
        count={selectedItems.length}
        onAddAll={handleAddAll}
      />
      <ItemPicker 
        items={filteredItems} 
        onAddItem={handleAddItem}
        onSearch={handleSearch}
        searchTerm={searchTerm}
      />
      <ItemsSelected 
        selectedItems={selectedItems}
        onRemoveItem={handleRemoveItem}
      />
    </div>
  );
}

export default App;

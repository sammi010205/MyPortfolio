import React from "react";
import ItemRow from "./ItemRow";

// ItemPicker component displays the list of available items with search functionality
// Props:
// - items: Array of available items to display
// - onAddItem: Function to handle adding an item to selected list
// - onSearch: Function to handle search input changes
// - searchTerm: Current search term for filtering items
export default function ItemPicker({ items, onAddItem, onSearch, searchTerm }) {
  return (
    <div className="item-picker h-auto">
      {/* Search input field for filtering items by name or department */}
      <input
        type="text"
        name="name"
        id="name"
        className="block w-full border-0 border-b border-transparent bg-gray-50 focus:border-blue-600 focus:ring-0 sm:text-sm h-12 pl-3"
        placeholder="Search by name or department"
        value={searchTerm}
        onChange={(e) => onSearch(e.target.value)}
      />

      {/* Scrollable container for the list of available items */}
      <div className="flow-root mt-8 overflow-y-auto h-96">
        <ul className="-my-5 divide-y divide-gray-200">
          {/* Map through filtered items and render each as an ItemRow */}
          {items.map((item, i) => (
            <ItemRow 
              key={`${i}-${item.name}`} 
              item={item} 
              onAddItem={onAddItem}
            />
          ))}
        </ul>
      </div>
    </div>
  );
}

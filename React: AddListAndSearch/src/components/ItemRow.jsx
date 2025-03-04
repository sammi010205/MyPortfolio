import React from "react";

export default function ItemRow({ item, onAddItem }) {
  return (
    <li className="py-4" aria-label={`item-${item.name}`} role="listitem">
      <div className="flex items-center space-x-4">
        <div className="flex-shrink-0">
          <img className="h-8 w-8 rounded-full" src={item.imageUrl} alt="" />
        </div>
        <div className="flex-1 min-w-0">
          <p className="text-sm font-medium text-gray-900 truncate">
            {item.name}
          </p>
          <p className="text-sm text-gray-500 truncate">{item.subTitle}</p>
        </div>
        <div className="pr-5">
          <button
            type="button"
            aria-label={`Add ${item.name}`}
            className="inline-flex items-center px-2.5 py-1.5 border border-transparent text-xs font-medium rounded text-indigo-700 bg-indigo-100 hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            onClick={() => {
              console.log(`Button clicked: Adding ${item.name}`);
              onAddItem(item);
            }}
          >
            +
          </button>
        </div>
      </div>
    </li>
  );
}

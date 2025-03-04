I will implement functionality for an item picker and a selected items list using React:

Task 1: Adding an Item
- When a user clicks the + button next to an item in the ItemPicker component, the item should be moved to the ItemsSelected component (the selected items list).
- Once an item is moved to the selected list, it should no longer appear in the ItemPicker component.

Task 2: Add All Items
-	Clicking the Add All button in the Header component should move all items from the ItemPicker list to the ItemsSelected list.
-	All items should be removed from the picker and appear in the selected items list.

Task 3: Removing an Item
-	In the ItemsSelected component, each item should have an X button next to it.
-	Clicking the X button should remove the item from the selected items list and return it to the ItemPicker list.

Task 4: Counter Header
- after adding an item the counter at the Header should increment, reflecting the total number of items in the selected list.
- deleting an item should also update this counter

Task 5: Search Functionalitty

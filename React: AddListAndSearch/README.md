# # quiz-08

Vide: https://www.loom.com/share/e951997100fb40e086b56d7307f48feb?sid=a479258e-3036-4ebb-beb2-ceb35393eda8

In this quiz, you will implement functionality for an item picker and a selected items list using React. You are given the initial structure with components but need to add functionality based on the following requirements:

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

[Optional Challenge - non graded]: Search Functionality
-	Implement a search input in the ItemPicker component.
-	When users type into the search field, the list of items should filter based on the input.
-	Items should be filtered by matching the name or the subtitle.

[Optional Challenge] Search Functionalitty
![CleanShot 2022-03-14 at 23 19 59](https://user-images.githubusercontent.com/1692542/158322554-1fe2663c-30d1-44dd-9cd4-eba58e55bd46.gif)


## Grading Criteria (10 points total)
1. Add Item Functionality (4 points):
  -	When a user clicks the + button next to an item in the ItemPicker component, the item should move to the ItemsSelected list.
  -	The item should no longer appear in the ItemPicker once it is selected.
2. Add All Functionality (1 point):
  -	When the user clicks the Add All button, all items from the ItemPicker should move to the ItemsSelected list.
  -	The ItemPicker should be empty after this action.
3. Remove Item Functionality (4 points):
  -	When a user clicks the X button next to an item in the ItemsSelected list, the item should move back to the ItemPicker list.
  -	The item should no longer appear in the ItemsSelected list.
4. Header counter (1 point)

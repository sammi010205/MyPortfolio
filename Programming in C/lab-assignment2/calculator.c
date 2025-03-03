//Fang Huang
//huang.fang@northeastern.edu

#include<stdio.h>

int main()
{
    int a,b,c, choice;
    
    printf("Enter your choice\n");
    printf(" 1. Addition\n 2. Subtraction\n 3. Multiplication\n 4. Division\n");
    scanf("%d",&choice);
    
    printf("Enter a and b values:  ");
    scanf("%d %d", &a, &b);
    
    switch(choice) {
    	case 1:
	  printf("Addition\n");
	  printf("Sum = %d\n",a+b);
	  break;
	case 2:
	  printf("Subtraction\n");
          printf("Difference = %d\n",a-b);
	  break;
	case 3:
	  printf("Multiplication\n");
          printf("Product = %d\n",a*b);
	  break;
	case 4:
	  if (b == 0) {
		  printf("Error: Divide by zero.\n");
		  printf("Quotient = 0\n");
	  }
	  else {
                  printf("Division\n");
		  printf("Quotient = %d\n",a/b);
	  }
	  break;
	default:
	  printf("Invalid option\n");
	  break;
    }
 	    
    return 0;
}

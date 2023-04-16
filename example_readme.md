
### Resources

The API includes the following resources:

-   `/` (HelloWorld): a GET request that returns a simple greeting message.
-   `/multiply` (Multiply): a GET request that takes two parameters (`num1` and `num2`) and returns their product.
-   `/calculator` and `/addition` (Calculator): a GET request that takes two parameters (`num1` and `num2`) and returns their sum, and a POST request that takes the same parameters and returns their difference.
-   `/abort` (Abort): a GET request that aborts with a custom error message.
-   `/not-realized-method` (NotRealizedMethod): a PUT request that returns a simple message.

### Examples

Here are some examples of how to interact with the API using cURL:

1.  Get greeting message:
    
    curl cli

    `curl 'http://localhost:5000/'`

    Output:

    
```jsonCopy code
{
    "message":"Hello, world!"
}
```  
2.  Multiply two numbers:
    
    curl cli

    `curl 'http://localhost:5000/multiply?num1=2.5\&num2=4.2'`

    Output:
    
    
    
```jsonCopy code
{
    "result":10.5
}
```
    
3.  Add two numbers:
    
    curl cli
    
    `curl 'http://localhost:5000/calculator?num1=3.5\&num2=4.2'`
    
    Output:
    
```jsonCopy code
{
    "result":7.7
}
```
    
4.  Subtract two numbers:
    
    curl cli
    
    `curl -X POST 'http://localhost:5000/calculator' -d "num1=3.5" -d "num2=4.2"`
    
    Output:

    
```jsonCopy code
{
    "result":-0.6999999999999993
}
 ```   
5.  Abort with custom error message:
    
    curl cli
    
    `curl 'http://localhost:5000/abort'`
    
    Output:
    
```jsonCopy code
{
    "message":"This is an error message."
}

```
    
6.  Use not realized method:
    
    curl cli
    
    `curl -X GET 'http://localhost:5000/not-realized-method'`
    
    Output:
    
```jsonCopy code
    
{
  "message": "Unimplemented method GET"
}
```
    

You can also interact with the API using other tools such as Postman or a web browser.
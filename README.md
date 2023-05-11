# INFO314-XMLRPC
A homework assignment for my INFO314 course.

## Goal
You must build a client and server for a calculator application using the XML-RPC "standard". You are free to do this in Java, Python, or any other language you prefer, but it must follow the structure and format dictated by the XML-RPC website.

## Background
[XML-RPC](http://xmlrpc.com/) was an early candidate during the "early web services" era, when we were just getting started exploring sending XML over HTTP. All endpoints are HTTP POST requests containing an XML payload that must follow the description given on the XML-RPC website.

```
POST /RPC2 HTTP/1.0
User-Agent: Frontier/5.1.2 (WinNT)
Host: betty.userland.com
Content-Type: text/xml
Content-length: 181

<?xml version="1.0"?>
<methodCall>
    <methodName>examples.getStateName</methodName>
    <params>
        <param>
            <value><i4>41</i4></value>
        </param>
    </params>
</methodCall>
```

The XML-RPC website has complete details, but in essence, all of the information about a remote call (or reponse) comes in the XML payload--it does not care about most of the rest of the HTTP layer.

## Server rubric (5 pts)

A basic scaffolded HTTP server (using the SparkJava project) is provided for you in the JavaServer directory. You are free to use this, or you can use a different project if you choose. Whatever you use, your HTTP endpoint must:

* listen on port 8080
* return a 404 for any URL other than "/RPC"
* return a 405 (Method Not Supported) for any operation other than POST
* the Host must reflect the hostname it is running on

Your XML-RPC endpoint must support five method names:

* `add`: it should take zero to any number of `i4` parameters, returning one `i4` result, adding the values together. `add` with 0 parameters should return 0; `add` with 1 parameter should return that original value. Otherwise, sum all the parameters.
* `subtract`: it should take two `i4` parameters, returning one `i4` result, subtracting the second from the first.
* `multiply`: it should take zero to any number of `i4` parameters, returning one `i4` result, multiplying the values together. `multiply` with 0 parameters should return 1; `multiply` with 1 parameter should return that original value. Otherwise, multiply all the parameters.
* `divide`: it should take two `i4` parameters, returning one `i4` result, dividing the first by the second. If the second parameter is a `0`, return a `faultCode` of `1` and a `faultString` of "divide by zero".
* `modulo`: it should take two `i4` parameters, returning one `i4` result, doing the modulo (remainder) operation. If the second parameter is a `0`, return a `faultCode` of `1` and a `faultString` of "divide by zero".

To be more clear about `add` and `multiply`, an `add` of `1, 2, 3, 4` should be 1 + 2 + 3 + 4, or 10, and a `multiply` of 1, 2, 3, 4 would be 1 * 2 * 3 * 4, or 24. 

If anything than an `i4` is passed to any of these endpoints, return a `faultCode` of `3` and a `faultString` of "illegal argument type".

## Client rubric (3 pts)

Your client must be a console application that takes command-line parameters like so:

`java CalcClient localhost 8080`

In other words, `args[0]` should be the server, and `args[1]` the port. The User-Agent header should be the name of your group. The client then needs to exercise all five of the operations, like so:

* subtract(12, 6) = 6
* multiply(3, 4) = 12
* divide(10, 5) = 2
* modulo(10, 5) = 0
* add(0) = 0
* add(1, 2, 3, 4, 5) = 15
* multiply(1, 2, 3, 4, 5) = 120

In addition, the client should make sure the server responds with errors appropriately:

* add two very large numbers such that it triggers an overflow
* multiply two very large numbers and trigger an overflow
* subtract taking two string parameters should trigger illegal argument faults
* divide any number by 0 and trigger a divide-by-zero fault

# Batch test Google's robots.txt

Batch test a list of URLs against Google's robots.txt parser and matcher

## About the library

This is a fork of [Google's robotstxt repo](https://github.com/google/robotstxt)

## Batch testing

First, [build the robots executable](#building-the-library) and then move the executable to the project base directory:

```bash
>>> mv c-build/robots ./
```

Add your pages and robots.txt to local files, e.g.

```bash
>>> cat test.urls.txt
https://example.com/
https://example.com/page
https://example.com/page/1
https://example.com/page/2
https://example.com/page/2?my_param=true
>>> cat test.robots.txt
User-Agent: *
Disallow: /page/1
Disallow: /page/*?my_param=true
```

Run the test

```bash
>>> python run_batch_test.py --robots-file test.robots.txt --url-file test.urls.txt
```

The result will be available in a file: `test.results.csv`

## Building the library

#### Building with CMake

[CMake](https://cmake.org) is the community-supported build system for the
library.

To build the library using CMake, just follow the steps below:

```bash
>>> mkdir c-build && cd c-build
...
>>> cmake .. -DROBOTS_BUILD_TESTS=ON
...
>>> make
...
>>> make test
```

## License

The robots.txt parser and matcher C++ library is licensed under the terms of the
Apache license. See LICENSE for more information.

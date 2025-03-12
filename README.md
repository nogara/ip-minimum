# IP Minimum

A utility tool that collapses IPv4 addresses and networks into the minimum set of /16 networks needed to cover all the input IPs.

## Description

IP Minimum is a command-line tool that reads lists of IPv4 addresses or networks (in CIDR notation) and collapses them into the minimum set of /16 networks that cover all the input addresses. This can be useful for optimizing firewall rules, ACLs, or routing tables where aggregation can simplify management.

## Features

- Converts individual IP addresses and CIDR blocks to a minimal set of /16 networks
- Handles mixed inputs of individual IPs and network blocks
- Automatically deduplicates overlapping networks
- Works with both file inputs and piped data

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/ip_minimum.git
cd ip_minimum
```

No special dependencies are required beyond Python 3.

## Usage

There are two ways to use the tool:

### Option 1: Provide a file containing IP addresses

```bash
python main.py path/to/ip_list.txt
```

### Option 2: Pipe input directly

```bash
cat ip_list.txt | python main.py
```

## Input Format

The input file should contain one IP address or CIDR notation network per line:

```
192.168.1.1
10.0.0.0/24
172.16.5.5
```

## Output

The tool outputs the minimized set of /16 networks:

```
Collapsed up to /16 coverage:
10.0.0.0/16
172.16.0.0/16
192.168.0.0/16
```

## Example

Input file `ips.txt`:
```
192.168.1.1
192.168.2.5
10.0.0.1
10.0.1.1
172.16.5.5
```

Command:
```bash
python main.py ips.txt
```

Output:
```
Collapsed up to /16 coverage:
10.0.0.0/16
172.16.0.0/16
192.168.0.0/16
```

## License

MIT License

Copyright (c) 2023

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

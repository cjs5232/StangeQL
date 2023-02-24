# CSCI.421 - Database System Implementation - Group Project
## Overview
- Project: Implement a database management system.
- Language:
  - Python
- Group Number:
  - 1
- Group Members
  - Gunnar Bachmann (ggb6130)
  - Aidan Mellin (atm3232)
  - Alex Cooley (arc7311)
  - Cindy Donch (cad7046)
  - Connor Stange (cjs5232)

## Project Structure
TODO

## Build Instructions
1. Open a terminal and navigate to the src/ directory of this project folder.
2. Execute the following command: ```python main.py <db_loc> <page_size> <buffer_size>```
- **Database Location** `<db_loc>`: The absolute path to the directory to store the database in;
including the trailing slash. This includes any page files and database stores.
  - Example: /home/abc/myDB/
- **Page**: A limited size (`<page_size>`, data store on a file system). Tables will be stored as
a file on the file system. These files will be made up of pages.
- **Page Buffer**: An in-memory buffer to store recently used pages. This has a size limit
`<buffer_size>`.
> **_NOTE:_** While the program is running and accepting queries, you may find the `help;` command useful. For Example:
```
JottQL> help;
```
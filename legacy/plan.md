1. Staff enter data from legacy xls to data_entry.ods. The data will hold Type, Size, Name, and Product information
2. Rename the columns to their valid Odoo attribute names: part_no -> Store Code
3. Add the following columns with default values: Date Added, Is Sold
4. Capitalize the first letter of each word in each cell
5. Type column can be filtered with a unique constraint to facilitate import into Odoo
6. Size column can be filtered with a unique constraint to facilitate import into Odoo
7. Import only the three relevant columns for the Name model
8. For the Product, the following must be done for its columns:
- Name - programmatically generate using generic_name and branded_name column
- Size - concatenate the Size and Type column
- Others - copy paste the columns  
9. Price and Pack must be entered manually either through Odoo or another valid excel file to be imported since there is no existing legacy data for Pack and Price that is complete
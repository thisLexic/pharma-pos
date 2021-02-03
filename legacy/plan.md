1. Staff enter data from legacy xls to data_entry.ods. The data will hold Type, Size, Name, and Product information
2. Type column can be filtered with a unique constraint to facilitate import into Odoo
3. Size column can be filtered with a unique constraint to facilitate import into Odoo
4. Import only the three relevant columns for the Name model
5. For the Product, the following must be done for its columns:
- Name - programmatically generate using generic_name and branded_name column
- Size - concatenate the Size and Type column
- Others - copy paste the columns  
6. Price and Pack must be entered manually either through Odoo or another valid excel file to be imported since there is no existing legacy data for Pack and Price that is complete
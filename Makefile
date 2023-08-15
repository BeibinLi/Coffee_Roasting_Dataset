move:
	mkdir -p data/database
	mv *.csv data/database
	mv *.sqlite data/database

db_gen:
	python database/gen_supply.py
	python database/gen_cafe.py
	python database/gen_sales_price_history.py
	python database/gen_supply_price.py
	python database/gen_employee.py
	python database/gen_demand_history.py
	python database/gen_roastery.py # the last step

convert:
	python database/csv_to_sql.py
  
full:
	make db_gen
	make convert
	make move
move:
	mkdir -p opti_coffee/database
	mv *.csv opti_coffee/database
	mv *.sqlite opti_coffee/database

db_gen:
	python gen_db/gen_supply.py
	python gen_db/gen_cafe.py
	python gen_db/gen_sales_price_history.py
	python gen_db/gen_supply_price.py
	python gen_db/gen_employee.py
	python gen_db/gen_demand_history.py
	python gen_db/gen_roastery.py # the last step

convert:
	python gen_db/csv_to_sql.py
  
full:
	make db_gen
	make convert
	make move

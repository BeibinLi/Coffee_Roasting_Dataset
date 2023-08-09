## Public: 
- [X] Intro and Services Document [Vector]
- [X] Pricing database: Bean and Coffee type [beibin]
- [X] Contact information Document [Vector]

## Private:
- Manufacturing Databases:
  - [X] History of supplier costs and quantity [beibin]
  - [X] History of demand price [beibin]
  - History of demand quantity [beibin]
  - Solver history [beibin]
- Financial Databases
  - [X] Employee and salary and performance [vector]
  - Cash Flow, balance sheet [beibin]
  - [X] Customer information [vector]
  - [X] Supplier information [beibin]
- Documents
  - Advertising
  - [X] Training Manuals: how to roast [beibin]
  - [X] Safety Manuals [beibin]
  - Machine Maintenance History and Schedule
  - Quality Control Manuals
- Codebase
  - [X] Solver-related documents [Beibin]
  - Visualization code  [vector]


## Question Answer Set

QUESTION:
What is the total quantity of {{VALUE-BEAN-TYPE}} available in {{VALUE-COUNTRY}}%?
VALUE-CAFE: random.choice(bean_types)
VALUE-NUMBER: random.choice(country_list)
GT CODE:
df1 = pd.read_csv("supplier_price_history.csv")
df2 = pd.read_csv("suppliers.csv")
df = df1.join(df2.set_index('supplier_id'), on='supplier_id')
df = df[df['bean_type'] == {{VALUE-BEAN-TYPE}}]
df = df[df['country'] == {{VALUE-COUNTRY}}]
print(df['quantity'].sum())
TYPE: demand-increase
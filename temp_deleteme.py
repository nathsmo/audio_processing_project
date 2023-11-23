import pandas as pd 

df = pd.DataFrame(columns=['user','section_number','average_hz_val','section_sigma', 
                           'section_std'])

# Save the dataframe to a CSV file
df.to_csv('section_outputs.csv', index=False)
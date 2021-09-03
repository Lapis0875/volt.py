import volt

field1 = volt.EmbedField('Field 1', 'I am a sample field!', False)
field1_copy = volt.EmbedField('Field 1', 'I am a sample field!', False)
field2 = volt.EmbedField('Field 2', 'I am another sample field!', True)

print('field1 == field1_copy', field1 == field1_copy)
print('field1 is field1_copy', field1 is field1_copy)
print('field1 == field2', field1 == field2)
print('field1 is field2', field1 is field2)

fields = [field1, field2]
print(fields)
fields.remove(field1_copy)
print(fields)

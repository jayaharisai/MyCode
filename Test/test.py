from MyCode import syntactic_data_generator, read_csv, MyCodeOpenaiWrapper, RagLoaders

pass_values = RagLoaders(
    file_path= "Complete-Guide-to-MLOps.pdf",
    multiple_file_path = ['Complete-Guide-to-MLOps.pdf', 'Complete-Guide-to-MLOps.pdf']
)

result = pass_values.start()
print(len(result))
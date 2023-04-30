from the_vault import app # type: ignore



# os.environ['ENV'] in ['development', 'production']
if __name__ == '__main__':
    app.run()
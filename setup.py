from cx_Freeze import setup,Executable
setup(name='My Apk',
      version='0.1',
      description='I am the world',
      executables=[Executable("XprtClient.py")])

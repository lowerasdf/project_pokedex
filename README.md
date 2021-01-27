# Project Pokedex
My dad once asked me to show him a couple of new pokemon. I made this full stack application to show him how new pokemon looks like based on their types. Only that the images are subject to copyright, so they are not shown here. This app consists of a backend service written in Go, a simple frontend view with html, and MySQL database to store the pokemon.

### Installation
Make sure you created your own database, and change the username, password, and the name of the database in [db_setup.py](/db_setup.py) Run <pre><code>python3 db_setup.py</code></pre> to convert the csv to your database. Then, run <pre><code>go run project_pokedex.go</code></pre> to start the backend server. To visualize, see [pokedex.html](pokedex.html)

### Acknowledgement
The csv data are taken from [this repo](https://github.com/veekun/pokedex)

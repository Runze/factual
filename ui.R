library(shiny)
library(leaflet)
library(rCharts)

categories = c('Education', 'Libraries', 'Parks', 'Beauty Products', 'Computers and Electronics',
               'Fashion', 'Food and Beverage', 'Shopping Centers and Malls', 'Home Improvement',
               'Personal Care', 'Arts', 'Bars', 'Entertainment', 'Food and Dining', 'Sports and Recreation',
               'Transportation', 'Travel')

shinyUI(navbarPage('Factual', id='factual',
                   
                   tabPanel('Interactive map',
                            div(class='outer',
                                tags$link(href='styles.css', rel='stylesheet'),
                                tags$script(src='gomap.js'),
                                
                                absolutePanel(id = 'controls', class = 'modal', fixed = TRUE, draggable = TRUE,
                                              top = 60, left = 'auto', right = 20, bottom = 'auto',
                                              width = 330, height = 'auto',
                                              
                                              h2('Explorer'),
                                              
                                              textInput('address', 'Enter address', value = ''),
                                              textInput('city', 'Enter city', value = 'Los Angeles'),
                                              textInput('state', 'Enter state', value = 'CA'),
                                              textInput('zipcode', 'Enter zipcode', value = '90071'),
                                              selectInput('category', 'Pick a category', categories, 'Food and Dining'),
                                              textInput('keyword', 'Or search with a key word', value = ''),
                                              textInput('radius', 'Radius (meters)', value = 500),
                                              submitButton('Submit')
                                              ),
                                chartOutput('map', 'leaflet')
                              )
                            ),
                   
                   tabPanel('Table', dataTableOutput('table'))
))
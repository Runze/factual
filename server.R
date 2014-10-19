library(plyr)
library(rCharts)
options(stringsAsFactors = F)

load(file = 'data/categories.RData')
shinyServer(function(input, output, session){
  #resolve lat and lon from address
  df_r = reactive({
    r = resolve_addr(input$address, input$city, input$state, input$zipcode)
    validate(
      need(!is.na(r[1]) & !is.na(r[2]), 'Unable to resolve address')
    )
    return(r)
  })
  
  #filter based on resolved lat and lon
  df_s = reactive({
    lat = df_r()$lat
    lon = df_r()$lon
    
    if (input$keyword == '') {
      #search based on category
      id = subset(categories, label == input$category)$id
      return(search_cat(lat, lon, id, input$radius))
    }
    else {
      #search based on keywords
      return(search_kw(lat, lon, input$keyword))
    }
  })
  
  #create formatted table for display on the other tab
  df_s_formatted = reactive({
    if (nrow(df_s()) > 0) {
      df = subset(df_s(), select = -c(latitude, longitude, popup, website))
    }
    else {
      df = data.frame(matrix(rep('', 6), nrow = 1))
    }
    names(df) = c('Name', 'Address', 'City', 'Hours', 'Phone', 'Website')
    return(df)
  })
  
  #create map
  output$map = renderMap({
    m = Leaflet$new()
    m$set(width = 1200, height = 700)
    m$setView(c(df_r()$lat, df_r()$lon), zoom = 15)
    
    #according to the author of rCharts, to add circles, data need to be converted into list first
    #source: https://github.com/ramnathv/rCharts/issues/205
    ls_s = toJSONArray2(df_s(), json = F)
    
    #the following code is also from the source linked above
    m$geoJson(toGeoJSON(ls_s, lat = 'latitude', lon = 'longitude'),
              onEachFeature = '#! function(feature, layer){
                layer.bindPopup(feature.properties.popup)
              } !#',
              pointToLayer =  "#! function(feature, latlng){
                return L.circleMarker(latlng, {
                  radius: 5,
                  fillColor: feature.properties.Color || '#ef3b2c',
                  color: '#fc4e2a',
                  weight: 2,
                  fillOpacity: 0.8
                })
              } !#" 
    )

    m$enablePopover(TRUE)
    m$fullScreen(TRUE)
    return(m)    
  })
  
  #create table
  output$table = renderDataTable(df_s_formatted(),
                                 options = list(bFilter = F, iDisplayLength = 10, bAutoWidth = F))
})
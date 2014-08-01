library(httr)
library(rjson)
library(plyr)
library(rPython)

#python functions to retrieve data from factual
#add factual and oauth modules to a folder under the app directory (to be bundled together when deployed)
python.exec('import sys')
python.exec("sys.path.extend(['package'])")

#perform oauth
python.exec('from factual import Factual')
python.exec('from factual.utils import circle')
python.exec("factual = Factual('<api key>', '<api secret>')") 
python.exec("places = factual.table('places')")

#function to resolve address
python.exec("def resolve(address, locality, region, postcode):
          return factual.resolve('places', {'address':address,'locality':locality,'region':region,'postcode':postcode}).data()")

#function to filter based on category, latitude, and longitude
python.exec("def filter(category, lat, lon, radius):
          return places.filters({'category_ids':{'$includes':category}}).geo(circle(lat, lon, radius)).limit(50).data()")

#function to filter based on keyword, latitude, and longitude
python.exec("def search(kw, lat, lon, radius):
          return places.search(kw).geo(circle(lat, lon, radius)).limit(50).data()")

#function to resolve address
resolve_addr = function(address = '', city = 'Los Angeles', state = 'CA', zipcode = '90071') {
  #first try to use factual to resolve
  fact_res = python.call('resolve', address, city, state, zipcode)
  df_resolve = data.frame(fact_res$latitude, fact_res$longitude)
  
  #if not found, try to use data science toolkit to resolve
  if (nrow(df_resolve) == 0) {
    full_addr = gsub(' ', '%20', paste(address, city, state, zipcode))
    url_ds = sprintf('http://www.datasciencetoolkit.org/maps/api/geocode/json?sensor=FALSE&address=%s', full_addr)
    dat = fromJSON(paste(GET(url_ds), collapse = ''))
    if (length(dat$results) > 0) {
      dat = dat$results[[1]]$geometry$location
      df_resolve = data.frame(dat['lat'], dat['lng'])  
    }
    else {
      #if still not found, return 0 lat and lon to output error
      df_resolve = data.frame(0, 0)
    }
  }
  
  names(df_resolve) = c('lat', 'lon')
  return(df_resolve)
}

#filter and search
#function to extract relevant fields
extract_fil = function(x) {
  return (x[c('name', 'address', 'locality', 'hours_display', 'tel', 'website', 'latitude', 'longitude')])
}

#function to remove special characts
clean_char = function(x) {
  if (typeof(x) == 'character') {
    x = gsub('[^[:graph:]]', ' ', x)  
  }
  return(x)
}

#function to parse data
parse_dat = function(dat) {  
  dat = lapply(dat, extract_fil)
  
  #remove records with null or na value
  nul_val = which(lapply(dat, function(x) any(as.logical(lapply(x, is.null)))) == T)
  if (length(nul_val) > 0) {
    dat[nul_val] = NULL
  }
  na_val = which(lapply(dat, function(x) any(as.logical(lapply(x, is.na)))) == T)
  if (length(na_val) > 0) {
    dat[na_val] = NULL
  }
  dat = ldply(dat, data.frame)
  
  #remove special characters
  dat = data.frame(lapply(dat, clean_char))  
  return(dat)
}

#filter based on category and lat and lon
search_cat = function(lat, lon, category = 338, radius = 500, limit = 50) {
  fact_fil = python.call('filter', category, lat, lon, radius)
  fact_fil = parse_dat(fact_fil)
  
  #add popup and website link
  if (nrow(fact_fil) > 0) {
    fact_fil$popup = sprintf('%s<br>%s<br>%s<br>%s<br>%s', fact_fil$name, fact_fil$address, fact_fil$locality, fact_fil$hours_display, fact_fil$tel)
    fact_fil$website_link = paste0("<a href='",  fact_fil$website, "' target='_blank'>Link</a>") 
  }
  return(fact_fil)
}

#filter based on keywords and lat and lon
search_kw = function(lat, lon, kw, radius = 500, limit = 50) {
  fact_kw = python.call('search', kw, lat, lon, radius)
  fact_kw = parse_dat(fact_kw)
  
  #add popup and website link
  if (nrow(fact_kw) > 0) {
    fact_kw$popup = sprintf('%s<br>%s<br>%s<br>%s<br>%s', fact_kw$name, fact_kw$address, fact_kw$locality, fact_kw$hours_display, fact_kw$tel)
    fact_kw$website_link = paste0("<a href='",  fact_kw$website, "' target='_blank'>Link</a>") 
  }
  return(fact_kw)
}
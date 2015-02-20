#!/usr/bin/python

import xml.sax

# expat parser

class StopHandler( xml.sax.ContentHandler ):
   def __init__(self):
      self.CurrentData = ""
      self.StopNo = ""
      self.StopDescription = ""
      self.year = ""
      self.rating = ""
      self.stars = ""
      self.description = ""

   # Call when an element starts
   def startElement(self, tag, attributes):
      self.CurrentData = tag
      if tag == "GetRouteSummaryForStopResult":
         print "*****GetRouteSummaryForStopResult*****"


   # Call when an elements ends
   def endElement(self, tag):
      if self.CurrentData == "StopNo":
         print "StopNo:", self.StopNo
      elif self.CurrentData == "StopDescription":
         print "StopDescription:", self.StopDescription
      #elif self.CurrentData == "year":
      #   print "Year:", self.year
      #elif self.CurrentData == "rating":
      #   print "Rating:", self.rating
      #elif self.CurrentData == "stars":
      #   print "Stars:", self.stars
      #elif self.CurrentData == "description":
      #   print "Description:", self.description
      #self.CurrentData = ""

   # Call when a character is read
   def characters(self, content):
      if self.CurrentData == "StopNo":
         self.StopNo = content
      elif self.CurrentData == "StopDescription":
         self.StopDescription = content
   #   elif self.CurrentData == "year":
   #      self.year = content
   #   elif self.CurrentData == "rating":
   #      self.rating = content
   #   elif self.CurrentData == "stars":
   #      self.stars = content
   #   elif self.CurrentData == "description":
   #      self.description = content
  
if ( __name__ == "__main__"):
   
   # create an XMLReader
   parser = xml.sax.make_parser()
   # turn off namepsaces
   parser.setFeature(xml.sax.handler.feature_namespaces, 0)

   # override the default ContextHandler
   Handler = MovieHandler()
   parser.setContentHandler( Handler )
   
   parser.parse("movies.xml")
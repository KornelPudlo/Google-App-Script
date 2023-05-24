# Hello World
# This Google App Script creates a dedicated ribbon tab in Google Sheets with several buttons that can be used to 
#   - show cell content
#   - unhide dedicated tab
#   - redirect user to dedicated, external website
#  What is more, it is assigned to a manually created button that:
#   - create a copy of a file and open it for user hence no need to use master version or create a copy manually
#   - once copy created, it unhides dedicated hidden tab
#   - stores a copy in dedicated Google Drive folder 
  
#   Feel free to use it but note that it will not be maintained anymore hence there might be some errors with it :) 
  
  






function onOpen() {
  var ui = SpreadsheetApp.getUi();
  ui.createMenu('Dedicated ribbon name')
    .addItem('Show cell content', 'showContent')
    .addItem('Go To tab', 'goToTab')
    .addItem('See the manual', 'openManual')
    .addToUi();
}

function showContent() {
  var cell = SpreadsheetApp.getActiveSpreadsheet().getActiveCell();
  var value = cell.getValue();
  Browser.msgBox(value);
}

function goToTab() {
  createCopyOfSheetAndOpen(); #Call the function to create a copy and open it
}

function openManual() {
  var htmlOutput = HtmlService.createHtmlOutput('<a href="put your link here to dedicated external website ( manual in this scenario) " target="_blank">CUSTOM Message here for users once clicked</a>')
      .setWidth(300)
      .setHeight(150);
  SpreadsheetApp.getUi().showModalDialog(htmlOutput, 'Manual');
}

function createCopyOfSheetAndOpen() {
  var spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  var originalSheet = spreadsheet.getId();
  var originalName = spreadsheet.getName();
  var destinationFolderId = "google drive folder ID here";  #Replace with the destination folder ID where the copy will be saved
  
  var file = DriveApp.getFileById(originalSheet);
  var destinationFolder = DriveApp.getFolderById(destinationFolderId);
  
  var copy = file.makeCopy(originalName + " - Copy", destinationFolder);
  var newSpreadsheetId = copy.getId();
  var newSpreadsheetUrl = "https://docs.google.com/spreadsheets/d/" + newSpreadsheetId;
  
  var newSpreadsheet = SpreadsheetApp.open(copy);
  
  // Unhide the 'hidden tab name' sheet in the newly created copy
  var dsrSheet = newSpreadsheet.getSheetByName(' Hidden Tab Name');
  dsrSheet.showSheet();
  
  // Open the newly created copy
  SpreadsheetApp.setActiveSpreadsheet(newSpreadsheet);
  
  // Create a dialog with a clickable hyperlink
  var htmlOutput = HtmlService.createHtmlOutput('<script>window.open("' + newSpreadsheetUrl + '");google.script.host.close();</script>your custom message here');
  SpreadsheetApp.getUi().showModalDialog(htmlOutput, "Copy created successfully");
}

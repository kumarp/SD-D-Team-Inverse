// Chat client code.


// Keep track of the last message received (to avoid receiving the same message several times).
// This global variable is updated every time a new message is received.
var timestamp = 0;

// URL to contact to get updates.
var url = null;

// How often to call updates (in milliseconds)
var CallInterval = 2000;
// ID of the function called at regular intervals.
var IntervalID = 0;

// A callback function to be called to further process each response.
var prCallback = null;

// Variables used in InitRating()
var rate_value = 0;
var temp;

function callServer(){
	// At each call to the server we pass data.
	$.get(url, // the url to call.
			{time: timestamp}, // the data to send in the GET request.
			function(payload) { // callback function to be called after the GET is completed.
							processResponse(payload);
							},
			'json');
	};

function processResponse(payload) {
	// if no new messages, return.
	if(payload.status == 0) return;
	// Get the timestamp, store it in global variable to be passed to the server on next call.
	timestamp = payload.time;
	for(message in payload.messages) {
		$("#chatwindow").append(payload.messages[message].text);
	}
	// Scroll down if messages fill up the div.
	var objDiv = document.getElementById("chatwindow");
	objDiv.scrollTop = objDiv.scrollHeight;

	// Handle custom data (data other than messages).
	// This is only called if a callback function has been specified.
	if(prCallback != null) prCallback(payload);
}

function InitChatWindow(ChatMessagesUrl, ProcessResponseCallback){
/**   The args to provide are:
	- the URL to call for AJAX calls.
	- A callback function that handles any data in the JSON payload other than the basic messages.
	  For example, it is used in the example below to handle changes to the room's description. */

	$("#loading").remove(); // Remove the dummy 'loading' message.

	// Push the calling args into global variables so that they can be accessed from any function.
	url = ChatMessagesUrl;
	prCallback = ProcessResponseCallback;

	// Read new messages from the server every X milliseconds.
	IntervalID = setInterval(callServer, CallInterval);

	// The above will trigger the first call only after X milliseconds; so we
	// manually trigger an immediate call.
	callServer();

	// Process messages input by the user & send them to the server.
	$("form#chatform").submit(function(){
		// If user clicks to send a message on a empty message box, then don't do anything.
		if($("#msg").val() == "") return false;

		// We don't want to post a call at the same time as the regular message update call,
		// so cancel that first.
		clearInterval(IntervalID);

		$.post(url,
				{
				time: timestamp,
				action: "postmsg",
				message: $("#msg").val()
           		},
           		function(payload) {
         						$("#msg").val(""); // clean out contents of input field.
         						// Calls to the server always return the latest messages, so display them.
         						processResponse(payload);
       							},
       			'json'
       	);
       	
       	// Start calling the server again at regular intervals.
       	IntervalID = setInterval(callServer, CallInterval);
       	
		return false;
	});


} // End InitChatWindow

/**	This code below is an example of how to extend the chat system.
 * It's used in the second example chat window and allows us to manage a user-updatable
 * description field.
 *  */

// Callback function, processes extra data sent in server responses.
function HandleRoomDescription(payload) {
	$("#chatroom_description").text(payload.description);
}

function InitChatDescription(){

	$("form#chatroom_description_form").submit(function(){
		// If user clicks to send a message on a empty message box, then don't do anything.
		if($("#id_description").val() == "") return false;
		// We don't want to post a call at the same time as the regular message update call,
		// so cancel that first.
		clearInterval(IntervalID);
		$.post(url,
				{
				time: timestamp,
				action: "change_description",
				description: $("#id_description").val()
           		},
           		function(payload) {
         						$("#id_description").val(""); // clean out contents of input field.
         						// Calls to the server always return the latest messages, so display them.
         						processResponse(payload);
       							},
       			'json'
       	);
       	// Start calling the server again at regular intervals.
       	IntervalID = setInterval(callServer, CallInterval);
		return false;
	});

}

// Function to react to user clicking the "Submit Rating" button
function InitRating(){

    // when the POST is sent, submit
	$("form#ratingform").submit(function(){
        // Get the value of the radio button clicked
        rate_value = $('input:radio[name=rating]:checked').val();
        
        // Disable Submit button on click
        temp = $('input[type=submit]', this);
        temp.attr('disabled', 'disabled');
        
        // post by specifying that the post action is "rate" and the rating is the value from the radio button
		$.post(url,
				{
				time: timestamp,
				action: "rate",
				rating: rate_value
           		},
           		function(temp) {
                    // Disable Submit button on successful post
                    temp.attr('disabled', 'disabled');
       							},
       			'json'
       	);

		return false;
		
	});

}

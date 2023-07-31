let start = 0, timeCount = 0, timeCountStorage = [], finalDistanceStorage = [], USCounter, i = false

document.addEventListener("keydown", function(keyevent){
	recordTextElement = document.getElementById("RecordingText")
	switch(keyevent.keyCode){
		case 32: // '{space}'
			console.log("Time Printed: "+timeCount)
			break;
		case 13: // '{enter}'
			i = !i
			if(i)
				document.getElementById("SourceVideo").src = "/video_feed" //"{{ url_for('video_feed') }}"
			else
				document.getElementById("SourceVideo").src = "/video_feed_contours" //"{{ url_for('video_feed_contours') }}"
			console.log(i);
			break;
		case 81: // 'Q'
			console.log("Timer started!");
			start = Math.round(Date.now()/1000);
			recordTextElement.innerHTML = "Recording Status: Recording..."
			recordTextElement.style.color = "lime";
			break;
		case 69: // 'E'
			console.log("Timer stopped!");
			timeCount = Math.round(Date.now()/1000)-start;
			timeCountStorage.push(timeCount);
			finalDistanceStorage.push(USCounter);
			recordTextElement.innerHTML = "Recording Status: Recorded."
			recordTextElement.style.color = "red";
			break;
		default:
			console.log("TimeCountStorage: "+timeCountStorage+"\nfinalDistanceStorage: "+finalDistanceStorage)
			break;
	};
});

function PrintTimeHistory(){
	Area = document.getElementById("HistArea")
	Area.style.height = "0px";
	Area.innerHTML = "";
	for(let i = 0; i < timeCountStorage.length; i++){
		Area.innerHTML += "Object #"+String(i+1)+"<br>Time: "+String(timeCountStorage[i])+"sec(s)<br>Final Distance: ~"+String(finalDistanceStorage[i])+"cm <br><br>";
		Area.style.height = String(1+Area.scrollHeight)+"px"; 
	}
}

var IntId = setInterval(updateDistance, 700)
function updateDistance(){
	$.ajax({url: '/_getDist'}).done((data) => {
		USCounter = Math.round(data.d*10)/10
	});
}

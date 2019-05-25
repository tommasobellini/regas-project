var count = null;
var chatSocket = new WebSocket(
    'ws://' + window.location.host +
    '/ws/core/');

window.setInterval(myfunc = function () {
    var onlinePoint = document.getElementById('onlinePoint');
    if((Date.now() - count) < 8000) {
        console.log("Is running");
        onlinePoint.style = 'border: 10px solid lightgreen;'
    }else{
        console.log('is not running');
        onlinePoint.style = 'border: 10px solid red;'
    }
}, 5000);

var data_list = [];
var data_list2 = [];
var data_list3 = [];

google.charts.load('current', {packages: ['corechart', 'line']});
chatSocket.onmessage = function(e) {
    count = Date.now();
    var data = JSON.parse(e.data);

    var humidity_data = data['humidity'];
    var temperature_data = data['temperature'];
    var datetime = data['datetime'];
    var date = datetime.split(' ')[0];
    var time = datetime.split(' ')[1];
    var year = date.split('-')[0];
    var month = date.split('-')[1];
    var day = date.split('-')[2];
    var hour = time.split(':')[0];
    var minute = time.split(':')[1];
    var second = time.split(':')[2];
    if(data_list.length === 10){
        data_list.shift()
    }
    data_list.push([ new Date(year,month,day,hour,minute,second).toLocaleTimeString(),parseFloat(humidity_data.split('%')[0],10)])
    if(data_list2.length === 10){
        data_list2.shift()
    }
    data_list2.push([ new Date(year,month,day,hour,minute,second).toLocaleTimeString(),parseFloat(temperature_data.split('°C')[0],10)])
    if(data_list3.length === 10){
        data_list3.shift()
    }
    data_list3.push([ new Date(year,month,day,hour,minute,second).toLocaleTimeString(),parseFloat(temperature_data.split('°C')[0],10),parseFloat(humidity_data.split('%')[0],10)])

  google.charts.setOnLoadCallback(drawCurveTypes);
  google.charts.setOnLoadCallback(drawCurveTypes2);
  google.charts.setOnLoadCallback(drawCurveTypes3);

  function drawCurveTypes() {
      var data = new google.visualization.DataTable();
      data.addColumn('string', 'Time');
      data.addColumn('number', 'Humidity');
      data.addRows(data_list);

      var options = {
        hAxis: {
          title: 'TimeLine'
        },
        vAxis: {
          title: 'Humidity'
        },
        series: {
          1: {curveType: 'function'}
        }
      };

      var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
      chart.draw(data, options);
    }
    function drawCurveTypes2() {
      var data = new google.visualization.DataTable();
      data.addColumn('string', 'Time');
      data.addColumn('number', 'Temperature');
      data.addRows(data_list2);

      var options = {
        hAxis: {
          title: 'TimeLine'
        },
        vAxis: {
          title: 'Temperature'
        },
        series: {
          0: {curveType: 'function',color: 'red'}
        },
        'is3D':true,

      };

      var chart = new google.visualization.LineChart(document.getElementById('chart_div2'));
      chart.draw(data, options);
    }

    function drawCurveTypes3() {
      var data = new google.visualization.DataTable();
      data.addColumn('string', 'Time');
      data.addColumn('number', 'Temperature');
      data.addColumn('number', 'Humidity');
      data.addRows(data_list3);

      var options = {
        hAxis: {
          title: 'TimeLine'
        },
        vAxis: {
          title: 'Temperature'
        },
        series: {
          0: {curveType: 'function',color: 'blue'},
          1: {curveType: 'function',color: 'red'}
        },
        'is3D':true,

      };

      var chart = new google.visualization.LineChart(document.getElementById('chart_tot'));
      chart.draw(data, options);
    }
    var hum_elem = document.getElementById('humidity');
    var temp_elem = document.getElementById('temp');

    hum_elem.textContent = humidity_data;
    temp_elem.textContent = temperature_data;

    var s = Snap('#animated');
    var progress = s.select('#progress');
    var temp_data = document.getElementById('temp');
    if (temp_data.textContent.split('°C')[0] < 30)
        progress.attr({'stroke': 'blue'});
    if (temp_data.textContent.split('°C')[0] >= 30)
        progress.attr({'stroke': 'red'});
    progress.attr({strokeDasharray: '0, 100'});
    Snap.animate(0,251.2, function( value ) {
        progress.attr({ 'stroke-dasharray':value+',251.2'});
    }, 1000);

    var s2 = Snap('#animated2');
    var progress2 = s2.select('#progress2');
    var hum_data = document.getElementById('humidity');
    if (hum_data.textContent.split('%')[0] < 50)
        progress2.attr({'stroke': 'blue'});
    if (hum_data.textContent.split('%')[0] > 50)
        progress2.attr({'stroke': 'red'});
    progress2.attr({strokeDasharray: '0, 251.2'});
    Snap.animate(0,251.2, function( value ) {
        progress2.attr({ 'stroke-dasharray':value+',251.2'});
    }, 1000);
};
switchButtonClick = function () {
    var switchButton = document.getElementById('myonoffswitch');
    if(switchButton.checked === true){
        var bodyTag = document.getElementsByTagName('body')[0];
        bodyTag.style = 'background-image: url("../media/images/background_dark.jpg") ;\n' +
            '        background-position: center;\n' +
            '        background-repeat: no-repeat; color: white;';
        var colorSwitchClass = document.getElementsByClassName('colorSwitch');
        var i=0;
        for(i; i < colorSwitchClass.length; i++){
            colorSwitchClass[i].style = 'background-color: rgba(0,0,0, 0.7)'
        }
    } else {
        var menu = document.getElementsByClassName('menu-button')[0];
        menu.style = 'background-color:transparent;'
        var bodyTag = document.getElementsByTagName('body')[0]
        bodyTag.style = 'background-image: url("../media/images/background_white.jpg") ;\n' +
            '        background-position: center;\n' +
            '        background-repeat: no-repeat; color: #000000';
        colorSwitchClass = document.getElementsByClassName('colorSwitch');
        var i=0;
        for(i; i < colorSwitchClass.length; i++){
            colorSwitchClass[i].style = 'background-color: rgba(0,0,0, 0.3)'
        }
    }
};
switchButtonClick2 = function () {
    var switchButton = document.getElementById('splitGraphs');
    var chart_tot = document.getElementById('chart_tot');
    var chart_1 = document.getElementById('chart_div');
    var chart_2 = document.getElementById('chart_div2');
    if(switchButton.checked === true){
        chart_tot.style = 'animation: 3s joinGraph forwards'
        chart_1.style = 'opacity:0; animation: 1s displayAppear 1s forwards';
        chart_2.style = 'opacity:0; animation: 2s displayAppear 1s forwards'

        setTimeout(function () {
            chart_tot.classList.add('chart_totClass')
            chart_2.classList.remove('chart_totClass')
            chart_1.classList.remove('chart_totClass')
        }, 2100);
    } else {
        chart_2.style = 'animation: 3s joinGraph forwards'
        chart_1.style = 'animation: 2s joinGraph2 forwards'
        chart_tot.classList.remove('chart_totClass')

        chart_tot.style = 'animation: 3s displayAppear 2s forwards'
        setTimeout(function () {
            chart_2.classList.add('chart_totClass')
            chart_1.classList.add('chart_totClass')
        }, 2100);
    }
}
function w3_open() {
  document.getElementsByClassName("menu-button")[0].style.opacity = "0";
  document.getElementById("mySidebar").style.display = "block";
  document.getElementById(    "content").style = "transform: scaleX(0.85) translate(20vh)";


}

function w3_close() {
  document.getElementsByClassName("menu-button")[0].style.opacity = "1";
  document.getElementById("mySidebar").style.display = "none";
  document.getElementById(    "content").style = "";
}


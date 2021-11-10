<html>
    <head>
        <link rel="stylesheet" href="css/select.css">
        <?php
            ini_set('memory_limit', '-1');

            $listIXP = array();

            //Txt in to an array
            $fileOpen = fopen('outputs/list_IXPs.txt','r');
            if (!$fileOpen){
                echo 'ERROR: No ha sido posible abrirsdsds el archivo. Revisa su nombre y sus permisos.'; exit;
            }

            $index = 0; // contador de líneas
            while (!feof($fileOpen)) { // loop hasta que se llegue al final del archivo
                $line = trim(fgets($fileOpen)); // guardamos toda la línea en $line como un string
                if(strlen($line) > 2){
                    $listIXP[$index] = explode(";",$line);
                    $fileOpen++; // necesitamos llevar el puntero del archivo a la siguiente línea
                    $index++;
                }
            }

            sort($listIXP);

           

            $lastYearASNsv4 = array();
            for ($i=0; $i < count($listIXP); $i++) {
                if (file_exists('outputs/16_comparison_behavior_lastmonth_better/Comparison_members_behavior_'.$listIXP[$i][0].'.txt') == 0) {
                    $file = fopen('outputs/16_comparison_behavior_lastmonth_better/Comparison_members_behavior_'.$listIXP[$i][0].'.txt', "w");
                    fwrite($file, "" . PHP_EOL);
                    fclose($file);
                }
                $fileOpen = fopen('outputs/16_comparison_behavior_lastmonth_better/Comparison_members_behavior_'.$listIXP[$i][0].'.txt','r');
                if (!$fileOpen){
                    echo 'ERROR: No ha sido posible abrir el archivo '.$listIXP[$i][0].'. Revisa su nombre y sus permisos.'; exit;
                }

                $auxiliar = array();
                $index = 0; // contador de líneas
                while (!feof($fileOpen)) { // loop hasta que se llegue al final del archivo
                    $line = trim(fgets($fileOpen)); // guardamos toda la línea en $line como un string
                    if(strlen($line)>5){
                        $list = explode(";",$line);
                        $auxiliar[trim($list[0])][trim($list[1])] = trim($list[2]);                 
                    }
                    $fileOpen++; // necesitamos llevar el puntero del archivo a la siguiente línea
                }

                $list2 = array();
                $list2[0] = ['Washington_US',$auxiliar['Washington_US']['IXPShorterThanUpstream'],$auxiliar['Washington_US']['IXPBalancedUpstream'],$auxiliar['Washington_US']['IXPLongerThanUpstream']];
                $list2[1] = ['Japan_DIXIE',$auxiliar['Japan_DIXIE']['IXPShorterThanUpstream'],$auxiliar['Japan_DIXIE']['IXPBalancedUpstream'],$auxiliar['Japan_DIXIE']['IXPLongerThanUpstream']];
                $list2[2] = ['London_LINX',$auxiliar['London_LINX']['IXPShorterThanUpstream'],$auxiliar['London_LINX']['IXPBalancedUpstream'],$auxiliar['London_LINX']['IXPLongerThanUpstream']];
    
                $lastYearASNsv4[$i] = $list2;
                
            }

            
            
    
        ?>
        <script type="text/javascript" src="//cdnjs.cloudflare.com/ajax/libs/jquery/2.0.3/jquery.min.js"></script>
        <script type="text/javascript" src="https://www.google.com/jsapi"></script>
        <script type="text/javascript">
    
            var listIXP = (<?php echo json_encode($listIXP)?>);
            //var lastMonthASNs = (<?php echo json_encode($lastMonthASNs)?>);
            var lastYearASNs_v4 = (<?php echo json_encode($lastYearASNsv4)?>);
            var porcentaje1 = [];
            var porcentaje2 = [];

            var multiYearASNs = (<?php echo json_encode($multiYearASNs)?>);
            var charge = 0;

            google.load("visualization", "1", {packages:["corechart"]});
            google.setOnLoadCallback(paint);

            for (var i = 0; i < lastYearASNs_v4.length; i++) {
                for (var j = 0; j < lastYearASNs_v4[i].length; j++) {
                    console.log(lastYearASNs_v4[j][0])
                    if (lastYearASNs_v4[j][0][0] == 'Washington_US') {
                        lastYearASNs_v4[j][0][0] = "APNIC's router in Washington, US"
                    };
                    if (lastYearASNs_v4[j][1][0] == 'Japan_DIXIE') {
                        lastYearASNs_v4[j][1][0] = "APNIC's router at DIX-IE, Japan"
                    };
                    if (lastYearASNs_v4[j][2][0] == 'London_LINX') {
                        lastYearASNs_v4[j][2][0] = "Bhutan Telecom's router at LINX, London"
                    };
                    lastYearASNs_v4[i][j][1] = parseInt(lastYearASNs_v4[i][j][1]);
                    lastYearASNs_v4[i][j][2] = parseInt(lastYearASNs_v4[i][j][2]);
                    lastYearASNs_v4[i][j][3] = parseInt(lastYearASNs_v4[i][j][3]);
                };
            };

            function paint() {

                var seleccionado = document.getElementById("selectIXP");
                var numero = seleccionado.selectedIndex;

                if (numero == 0) {
                    drawChart(numero);
                }else{
                    drawChart(numero-1);
                    var titulo = document.getElementById("titulo1");
                    IXP = (seleccionado.value).split(",")[0]; 
                    titulo.innerHTML = "Unbalanced announcement : "+IXP+" vs. Upstream ";
                }
            }

            function drawChart(i) {
                /*.........................*/
                var data = new google.visualization.DataTable();
                data.addColumn('string', 'Years');
                data.addColumn('number', 'Shorter (Pref [IXP] > Pref [Upstream])');
                data.addColumn('number', 'Balanced (Pref [IXP] = Pref [Upstream])');
                data.addColumn('number', 'Longer (Pref [IXP] < Pref [Upstream])');

                data.addRows(lastYearASNs_v4[i]);

                var options = {
                    animation:{ duration: 1000,
                                easing: 'out',
                                startup: true},
                    width: 1000,
                    height: 300,
                    hAxis: {
                        title: 'Upstream/International Looking Glass', 
                        textStyle:{fontName: 'Trebuchet MS', fontSize: '10'},
                        titleTextStyle:{fontName: 'Trebuchet MS'}},
                    vAxis: {
                        viewWindow:{ min: 0 },
                        title: 'Number of prefixes',
                        textStyle:{fontName: 'Trebuchet MS'},
                        titleTextStyle:{fontName: 'Trebuchet MS'}},
                    legend: {textStyle:{fontName: 'Trebuchet MS' , fontSize: '10'}},
                    tooltip: {textStyle:{fontName: 'Trebuchet MS'}},
                    colors: ['#53A8FB', '#F1CA3A', 'green'],
                };

                var chart =  new google.visualization.ColumnChart(document.getElementById('originASNs'));
                chart.draw(data, options);
            }

            function chargeList(){
                if (charge== 0) {
                    var sel = document.getElementById('selectIXP');
                    for (var i = 0; i <listIXP.length; i++) {
                        var opt = document.createElement('option');
                        opt.innerHTML = listIXP[i][0]+" ("+listIXP[i][1]+")";
                        opt.value = listIXP[i];
                        sel.appendChild(opt);
                    }
                }
                charge = 1;
            }

           $(window).resize(function () {
                resize();
            });

            $(document).ready(function(){
                resize();
            });

            var designWidth = 1100;

            function resize() {
                var w = $(window).width();
                var zoom = parseInt(w / designWidth * 100).toString() + "%";
                $("#content").css("zoom", zoom);
            }

            function descarga1(){
                console.log("adddd")
                var seleccionado = document.getElementById("selectIXP");
                var numero = seleccionado.selectedIndex;
                if (numero == 0) {
                    alert("Select an IXP");
                }else{
                    IXP = (seleccionado.value).split(",")[0];
                    console.log (IXP)
                    $.ajax({
                        type: 'HEAD',
                        url: 'outputs/16_comparison_behavior_lastmonth_better/List_prefix_announcements_IXPBalancedUpstream__for__'+IXP+'.txt',
                        success: function() {
                            downloadURI('outputs/16_comparison_behavior_lastmonth_better/List_prefix_announcements_IXPBalancedUpstream__for__'+IXP+'.txt',IXP+'_IXPBalancedUpstream.txt');
                        },  
                        error: function() {
                        
                        }
                    });
                    $.ajax({
                        type: 'HEAD',
                        url: 'outputs/16_comparison_behavior_lastmonth_better/List_prefix_announcements_IXPLongerThanUpstream__for__'+IXP+'.txt',
                        success: function() {
                            downloadURI('outputs/16_comparison_behavior_lastmonth_better/List_prefix_announcements_IXPLongerThanUpstream__for__'+IXP+'.txt',IXP+'_IXPLongerThanUpstream.txt');
                        },  
                        error: function() {
                        
                        }
                    });
                    $.ajax({
                        type: 'HEAD',
                        url: 'outputs/16_comparison_behavior_lastmonth_better/List_prefix_announcements_IXPShorterThanUpstream__for__'+IXP+'.txt',
                        success: function() {
                            downloadURI('outputs/16_comparison_behavior_lastmonth_better/List_prefix_announcements_IXPShorterThanUpstream__for__'+IXP+'.txt',IXP+'_IXPShorterThanUpstream.txt');
                        },  
                        error: function() {
                        
                        }
                    });
                }
                
            }

            function downloadURI(uri,name) {
                var link = document.createElement("a");
                link.download = name;
                link.href = uri;
                link.click();
            }

        </script>
        <style type="text/css">
            body{
                line-height: 1px;
            }
            #originASNs {
                height:1em
                line-height: 1px;
                margin-left: 50px;
            }
            #multiyear {
                margin-left: 50px;
            }
            #lastyear {
                margin-left: 50px;
            }
            #separador {
                margin-top: 40px;
            }
            #select{
                margin: 10px;
                margin-left: 530px
            }
            #visibleASNs{
                margin-left: 100px;
            }
            #prefixes{
                margin-left: 100px;
            }
            #parrafos{
                margin-left: 200px;
            }

            .titulo{
                font-size: 17px;
                font-family: 'Trebuchet MS';
                font-weight: 400;
                color: #757575;
            } 

            #subtitulo{
                font-size: 14px;
                font-family: 'Trebuchet MS';
                color: #BDBDBD;
            }
            #botonDescarga{
                top: 100px;
                margin-left: 900px;
                font-size: 12px;
                font-family: 'Trebuchet MS'
            }
        </style>

    </head>
    <body>
        <div id="content">
            <div id ="select">
                <select name="selectIXP" id='selectIXP' onFocus='chargeList();' onClick='paint()'>
                    <option><b>Select IXP :</b></option>
                </select>
            </div>
            <div id="separador"></div>
            <div>
                <div id="parrafos">
                    <p class ="titulo" id="titulo1">Unbalanced announcement : IXP vs. Upstream </p>     
                    <p id="subtitulo">Over the last month</p>
                </div>
                <div id="originASNs" style="width: 1000px; height: 300px;"></div>
                <div id= "botonDescarga">
                   <img onclick="javascript:descarga1();"id="enlaceDesgarga" src="images/dbutton.png" height="30">
                </div>
            </div>

        </div>
    </body>
</html>

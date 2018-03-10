<html>
    <head>
        <link rel="stylesheet" href="css/select.css">
        <?php
            ini_set('memory_limit', '-1');

            $multiYearASNsv4 = array();
                if (file_exists('outputs_Regional_View/12_local_external_ASNs_multiyear/Percentage_Origin_ASNs_by_region.txt') == 0) {
                    $file = fopen('outputs_Regional_View/12_local_external_ASNs_multiyear/Percentage_Origin_ASNs_by_region.txt', "w");
                    fwrite($file, "" . PHP_EOL);
                    fclose($file);
                } 
                $fileOpen = fopen('outputs_Regional_View/12_local_external_ASNs_multiyear/Percentage_Origin_ASNs_by_region.txt','r');
                if (!$fileOpen){
                    echo 'ERROR: No ha sido posible abrir elkjhkjh archivo. Revisa su nombre y sus permisos.'; exit;
                }

                for ($z = 0; $z <= intval(date("Y"))-2005; $z++) {
                    $years[] = (string)(intval(date("Y"))-$z);
                }

                $prueba = array();
                for ($z=0; $z < count($years); $z++) { 
                    $prueba[$z] = $years[$z].';0;0;0;0;0;0;0;0';
                }

                $prueba = array_reverse($prueba);
                $plantilla = array();
                for ($k=0; $k < intval(date("Y"))-2004; $k++) { 
                    $plantilla[$k] = explode(";",$prueba[$k]);
                }

                $list =  array();
                $informacion = array();
                $index = 0; // contador de líneas
                while (!feof($fileOpen)) { // loop hasta que se llegue al final del archivo
                    $line = trim(fgets($fileOpen)); // guardamos toda la línea en $line como un string
                    $pos = strpos($line, "#");
                    if ($pos === false || strlen($line)<4) {
                        $list = explode(";",$line);
                        $mes = $list[0];
                        $tipo = $list[1];
                        $informacion[trim($mes)][trim($tipo)] = trim($list[2]);
                    }
                    $fileOpen++; // necesitamos llevar el puntero del archivo a la siguiente línea
                }
                for ($k=0; $k < count($plantilla); $k++) { 
                  
                    if (array_key_exists($plantilla[$k][0], $informacion)){

                        $plantilla[$k][1] = $informacion[$plantilla[$k][0]][" Private ASNs"];
                        $plantilla[$k][2] = $informacion[$plantilla[$k][0]]["Reserved ASNs"];
                        $plantilla[$k][3] = $informacion[$plantilla[$k][0]]["Local AFRINIC ASNs"];
                        $plantilla[$k][4] = $informacion[$plantilla[$k][0]]["External AFRINIC ASNs"];
                        $plantilla[$k][5] = $informacion[$plantilla[$k][0]]["RIPE ASNs"];
                        $plantilla[$k][6] = $informacion[$plantilla[$k][0]]["ARIN ASNs"];
                        $plantilla[$k][7] = $informacion[$plantilla[$k][0]]["APNIC ASNs"];
                        $plantilla[$k][8] = $informacion[$plantilla[$k][0]]["LACNIC ASNs"];
                    }
                } 
                $multiYearASNs = $plantilla;
        ?>
        <script type="text/javascript" src="//cdnjs.cloudflare.com/ajax/libs/jquery/2.0.3/jquery.min.js"></script>
        <script type="text/javascript" src="https://www.google.com/jsapi"></script>
        <script type="text/javascript">
    
            var multiYearASNs= (<?php echo json_encode($multiYearASNs)?>);
            var charge = 0;

            google.load("visualization", "1", {packages:["corechart"]});
            google.setOnLoadCallback(paint);

            
            for (var i = 0; i < multiYearASNs.length; i++) {
                    multiYearASNs[i][0] = multiYearASNs[i][0];
                    multiYearASNs[i][1] = parseInt(multiYearASNs[i][1]);
                    multiYearASNs[i][2] = parseInt(multiYearASNs[i][2]);
                    multiYearASNs[i][3] = parseInt(multiYearASNs[i][3]);
                    multiYearASNs[i][4] = parseInt(multiYearASNs[i][4]);
                    multiYearASNs[i][5] = parseInt(multiYearASNs[i][5]);
                    multiYearASNs[i][6] = parseInt(multiYearASNs[i][6]);
                    multiYearASNs[i][7] = parseInt(multiYearASNs[i][7]);
                    multiYearASNs[i][8] = parseInt(multiYearASNs[i][8]);
                          
            };


            function paint() {

                    drawChart();
            }

            function drawChart() {

                 /*.........................*/
                var data = new google.visualization.DataTable();
                data.addColumn('string', 'Months');
                data.addColumn('number', 'Private ASNs');
                data.addColumn('number', 'Reserved ASNs');
                data.addColumn('number', 'Local AFRINIC');
                data.addColumn('number', 'External AFRINIC');
                data.addColumn('number', 'RIPE');
                data.addColumn('number', 'ARIN');
                data.addColumn('number', 'APNIC');
                data.addColumn('number', 'LACNIC');

                data.addRows(multiYearASNs);

                var options = {
                    animation:{ duration: 1000,
                                easing: 'out',
                                startup: true},
                    width: 1000,
                    height: 300,
                    hAxis: {
                        title: 'Years', 
                        textStyle:{fontName: 'Trebuchet MS', fontSize: '10'},
                        titleTextStyle:{fontName: 'Trebuchet MS'}},
                    vAxis: {
                        viewWindow:{ min: 0 },
                        title: 'Number of ASNs',
                        textStyle:{fontName: 'Trebuchet MS'},
                        titleTextStyle:{fontName: 'Trebuchet MS'}},
                    legend: {position: 'top',textStyle:{fontName: 'Trebuchet MS'}},
                    tooltip: {textStyle:{fontName: 'Trebuchet MS'}},
                    isStacked: 'percent',
                    colors: ['blue', '#C44441', '#8CBC4F', '#7A5892', 'green', '#F48533', '#8BAAD1', 'yellow']
                };

                var chart = new google.visualization.ColumnChart(document.getElementById('lastYear'));
                chart.draw(data, options);

                
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

            function descarga2(){
                
                downloadURI('outputs_Regional_View/12_local_external_ASNs_multiyear/files_origin/APNIC_ASNs_all_IXPs_in_Africa.txt','APNIC_ASNs_all_IXPs_in_Africa.txt');
                downloadURI('outputs_Regional_View/12_local_external_ASNs_multiyear/files_origin/ARIN_ASNs_all_IXPs_in_Africa.txt','ARIN_ASNs_all_IXPs_in_Africa.txt');
                downloadURI('outputs_Regional_View/12_local_external_ASNs_multiyear/files_origin/Local_AFRINIC_ASNs_all_IXPs_in_Africa.txt','Local_AFRINIC_ASNs_all_IXPs_in_Africa.txt');
                downloadURI('outputs_Regional_View/12_local_external_ASNs_multiyear/files_origin/Private_ASNs_all_IXPs_in_Africa.txt','Private_ASNs_all_IXPs_in_Africa.txt');
                downloadURI('outputs_Regional_View/12_local_external_ASNs_multiyear/files_origin/Reserved_ASNs_ASNs_all_IXPs_in_Africa.txt','Reserved_ASNs_ASNs_all_IXPs_in_Africa.txt');
                downloadURI('outputs_Regional_View/12_local_external_ASNs_multiyear/files_origin/RIPE_ASNs_all_IXPs_in_Africa.txt','RIPE_ASNs_all_IXPs_in_Africa.txt');
    
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
                margin-top: 100px;
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
            <div id="parrafos">
                <p class ="titulo" id="titulo2">Distribution of non-local ASNs at all IXPs in Africa</p>     
                <p id="subtitulo">Per year over the historical Data (2005 up to now)</p>
            </div>
            <div id="lastYear" style="width: 1000px; height: 300px;"></div>
            <div id= "botonDescarga">
                   <img onclick="javascript:descarga2();" id="enlaceDesgarga" src="images/dbutton.png" height="30">
            </div>
        </div>
    </body>
</html>

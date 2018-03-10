<html>
    <head>
        <link rel="stylesheet" href="css/select.css">
        <?php
            ini_set('memory_limit', '-1');

            $listIXP = array();

            //Txt in to an array
           $listIXP = array();
            $listCC = array();

            //Txt in to an array
            $fileOpen = fopen('outputs/list_IXPs.txt','r');
            if (!$fileOpen){
                echo 'ERROR: No ha sido posible abrirsdsds el archivo. Revisa su nombre y sus permisos.'; exit;
            }

            $index = 0; // contador de líneas
            while (!feof($fileOpen)) { // loop hasta que se llegue al final del archivo
                $line = trim(fgets($fileOpen)); // guardamos toda la línea en $line como un string
                if(strlen($line) > 2){
                    $ixp = explode(";",$line);
                    $listIXP_aux[$index] = $ixp[1];
                    $fileOpen++; // necesitamos llevar el puntero del archivo a la siguiente línea
                    $index++;
                }
            }
            $listIXP = array_keys(array_flip($listIXP_aux));

             //Txt in to an array
            $fileOpen = fopen('outputs/list_IXPs.txt','r');
            if (!$fileOpen){
                echo 'ERROR: No ha sido posible abrirsdsds el archivo. Revisa su nombre y sus permisos.'; exit;
            }
            $index = 0; // contador de líneas
            while (!feof($fileOpen)) { // loop hasta que se llegue al final del archivo
                $line = trim(fgets($fileOpen)); // guardamos toda la línea en $line como un string
                if(strlen($line) > 2){
                    $ixp = explode(";",$line);
                    $listCC_aux[$index][0] = $ixp[1];
                    $listCC_aux[$index][1] = $ixp[2];
                    $fileOpen++; // necesitamos llevar el puntero del archivo a la siguiente línea
                    $index++;
                }
            }
               //echo json_encode($listCC_aux);
            $listCC = array_unique($listCC_aux, SORT_REGULAR);
            //echo json_encode($listCC);
            sort($listCC);
            
            $lastYearASNs = array();
            for ($i=0; $i < count($listCC); $i++) {
                if (file_exists('outputs_National_View/12_local_external_ASNs_lastyear/Percentage_Origin_ASNs_by_region_'.$listCC[$i][0].'.txt') == 0) {
                    $file = fopen('outputs_National_View/12_local_external_ASNs_lastyear/Percentage_Origin_ASNs_by_region_'.$listCC[$i][0].'.txt', "w");
                    fwrite($file, "" . PHP_EOL);
                    fclose($file);
                }
                $fileOpen = fopen('outputs_National_View/12_local_external_ASNs_lastyear/Percentage_Origin_ASNs_by_region_'.$listCC[$i][0].'.txt','r');
                if (!$fileOpen){
                    echo 'ERROR: No ha sido posible abrir el archivo '.$listCC[$i].'. Revisa su nombre y sus permisos.'; exit;
                }

                for ($z = 0; $z <= 12; $z++) {
                    $months[] = date("m-Y", strtotime( date( 'Y-m-01' )." -$z months"));
                }

                $prueba = array();
                for ($z=0; $z < count($months); $z++) {
                    $aux = explode("-",$months[$z]);
                    $aux[0] = (string)intval($aux[0]); 
                    $prueba[$z] = $aux[0].'-'.$aux[1].';0;0;0;0;0;0;0;0';
                }

                $prueba = array_reverse($prueba);
                $month = intval(date("m"));
                $plantilla = array();
                for ($k=0; $k < 13; $k++) { 
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
                        $plantilla[$k][1] = $informacion[$plantilla[$k][0]]["Private ASNs"];
                        $plantilla[$k][2] = $informacion[$plantilla[$k][0]]["Reserved ASNs"];
                        $plantilla[$k][3] = $informacion[$plantilla[$k][0]]["Local AFRINIC ASNs"];
                        $plantilla[$k][4] = $informacion[$plantilla[$k][0]]["External AFRINIC ASNs"];
                        $plantilla[$k][5] = $informacion[$plantilla[$k][0]]["RIPE ASNs"];
                        $plantilla[$k][6] = $informacion[$plantilla[$k][0]]["ARIN ASNs"];
                        $plantilla[$k][7] = $informacion[$plantilla[$k][0]]["APNIC ASNs"];
                        $plantilla[$k][8] = $informacion[$plantilla[$k][0]]["LACNIC ASNs"];
                    }
                } 
                $lastYearASNs[$i] = $plantilla;
            }

            $multiYearASNsv4 = array();
            for ($i=0; $i < count($listCC); $i++) {
                if (file_exists('outputs_National_View/12_local_external_ASNs_multiyear/Percentage_Origin_ASNs_by_region_'.$listCC[$i][0].'.txt') == 0) {
                    $file = fopen('outputs_National_View/12_local_external_ASNs_multiyear/Percentage_Origin_ASNs_by_region_'.$listCC[$i][0].'.txt', "w");
                    fwrite($file, "" . PHP_EOL);
                    fclose($file);
                } 
                $fileOpen = fopen('outputs_National_View/12_local_external_ASNs_multiyear/Percentage_Origin_ASNs_by_region_'.$listCC[$i][0].'.txt','r');
                if (!$fileOpen){
                    echo 'ERROR: No ha sido posible abrir elkjhkjh archivo '.$listCC[$i][0].'. Revisa su nombre y sus permisos.'; exit;
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
                        $plantilla[$k][1] = $informacion[$plantilla[$k][0]]["Private ASNs"];
                        $plantilla[$k][2] = $informacion[$plantilla[$k][0]]["Reserved ASNs"];
                        $plantilla[$k][3] = $informacion[$plantilla[$k][0]]["Local AFRINIC ASNs"];
                        $plantilla[$k][4] = $informacion[$plantilla[$k][0]]["External AFRINIC ASNs"];
                        $plantilla[$k][5] = $informacion[$plantilla[$k][0]]["RIPE ASNs"];
                        $plantilla[$k][6] = $informacion[$plantilla[$k][0]]["ARIN ASNs"];
                        $plantilla[$k][7] = $informacion[$plantilla[$k][0]]["APNIC ASNs"];
                        $plantilla[$k][8] = $informacion[$plantilla[$k][0]]["LACNIC ASNs"];
                    }
                } 
                $multiYearASNs[$i] = $plantilla;
            
            }
        ?>
        <script type="text/javascript" src="//cdnjs.cloudflare.com/ajax/libs/jquery/2.0.3/jquery.min.js"></script>
        <script type="text/javascript" src="https://www.google.com/jsapi"></script>
        <script type="text/javascript">
    
            var listIXP = (<?php echo json_encode($listIXP)?>);
            var listCC = (<?php echo json_encode($listCC)?>);
            var lastYearASNs= (<?php echo json_encode($lastYearASNs)?>);
            var multiYearASNs= (<?php echo json_encode($multiYearASNs)?>);
            var charge = 0;
            var month = new Array();
            month[0] = "Jan";
            month[1] = "Feb";
            month[2] = "Mar";
            month[3] = "Apr";
            month[4] = "May";
            month[5] = "Jun";
            month[6] = "Jul";
            month[7] = "Aug";
            month[8] = "Sep";
            month[9] = "Oct";
            month[10] = "Nov";
            month[11] = "Dec";

            google.load("visualization", "1", {packages:["corechart"]});
            google.setOnLoadCallback(paint);

            for (var i = 0; i < lastYearASNs.length; i++) {
                for (var j = 0; j < lastYearASNs[i].length; j++) {
                    aux = lastYearASNs[i][j][0].split("-");
                    aux[0] = month[parseInt(aux[0])-1];
                    lastYearASNs[i][j][0] = aux[0]+" "+aux[1]
                    lastYearASNs[i][j][1] = parseInt(lastYearASNs[i][j][1]);
                    lastYearASNs[i][j][2] = parseInt(lastYearASNs[i][j][2]);
                    lastYearASNs[i][j][3] = parseInt(lastYearASNs[i][j][3]);
                    lastYearASNs[i][j][4] = parseInt(lastYearASNs[i][j][4]);
                    lastYearASNs[i][j][5] = parseInt(lastYearASNs[i][j][5]);
                    lastYearASNs[i][j][6] = parseInt(lastYearASNs[i][j][6]);
                    lastYearASNs[i][j][7] = parseInt(lastYearASNs[i][j][7]);
                    lastYearASNs[i][j][8] = parseInt(lastYearASNs[i][j][8]);
                };
            };

            for (var i = 0; i < multiYearASNs.length; i++) {
                for (var j = 0; j < multiYearASNs[i].length; j++) {
                    multiYearASNs[i][j][0] = multiYearASNs[i][j][0];
                    multiYearASNs[i][j][1] = parseInt(multiYearASNs[i][j][1]);
                    multiYearASNs[i][j][2] = parseInt(multiYearASNs[i][j][2]);
                    multiYearASNs[i][j][3] = parseInt(multiYearASNs[i][j][3]);
                    multiYearASNs[i][j][4] = parseInt(multiYearASNs[i][j][4]);
                    multiYearASNs[i][j][5] = parseInt(multiYearASNs[i][j][5]);
                    multiYearASNs[i][j][6] = parseInt(multiYearASNs[i][j][6]);
                    multiYearASNs[i][j][7] = parseInt(multiYearASNs[i][j][7]);
                    multiYearASNs[i][j][8] = parseInt(multiYearASNs[i][j][8]);
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
                    var titulo2 = document.getElementById("titulo2");
                    IXP = (seleccionado.value).split(",")[0];
                    console.log('dedd')
                    titulo.innerHTML = "Distribution of non-local ASNs at "+IXP;
                    titulo2.innerHTML = "Distribution of non-local ASNs at "+IXP;
                }
            }

            function drawChart(i) {
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

                data.addRows(lastYearASNs[i]);

                var options = {
                    animation:{ duration: 1000,
                                easing: 'out',
                                startup: true},
                    width: 1000,
                    height: 300,
                    hAxis: {
                        title: 'Months', 
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

                var chart = new google.visualization.ColumnChart(document.getElementById('originASNs'));
                chart.draw(data, options);

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

                data.addRows(multiYearASNs[i]);

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

           function chargeList(){
                if (charge== 0) {
                    var sel = document.getElementById('selectIXP');
                    for (var i = 0; i <listCC.length; i++) {
                        var opt = document.createElement('option');
                        opt.innerHTML = listCC[i][1]+" ("+listCC[i][0]+")";
                        opt.value = listCC[i][0];
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
                        url: 'outputs_National_View/12_local_external_ASNs_lastyear/files_origin/APNIC_ASNs_'+IXP+'.txt',
                        success: function() {
                            downloadURI('outputs_National_View/12_local_external_ASNs_lastyear/files_origin/APNIC_ASNs_'+IXP+'.txt','Last_year_at_'+IXP+'_APNIC.txt');
                        },  
                        error: function() {
                        
                        }
                    });
                    $.ajax({
                        type: 'HEAD',
                        url: 'outputs_National_View/12_local_external_ASNs_lastyear/files_origin/RIPE_ASNs_'+IXP+'.txt',
                        success: function() {
                            downloadURI('outputs_National_View/12_local_external_ASNs_lastyear/files_origin/RIPE_ASNs_'+IXP+'.txt','Last_year_at_'+IXP+'_RIPE.txt');
                        },  
                        error: function() {
                        
                        }
                    });
                    $.ajax({
                        type: 'HEAD',
                        url: 'outputs_National_View/12_local_external_ASNs_lastyear/files_origin/ARIN_ASNs_'+IXP+'.txt',
                        success: function() {
                            downloadURI('outputs_National_View/12_local_external_ASNs_lastyear/files_origin/ARIN_ASNs_'+IXP+'.txt','Last_year_at_'+XP+'_ARIN.txt');
                        },  
                        error: function() {
                        
                        }
                    });
                    $.ajax({
                        type: 'HEAD',
                        url: 'outputs_National_View/12_local_external_ASNs_lastyear/files_origin/LACNIC_ASNs_'+IXP+'.txt',
                        success: function() {
                            downloadURI('outputs_National_View/12_local_external_ASNs_lastyear/files_origin/LACNIC_ASNs_'+IXP+'.txt','Last_year_at_'+IXP+'_LACNIC.txt');
                        },  
                        error: function() {
                        
                        }
                    });
                    $.ajax({
                        type: 'HEAD',
                        url: 'outputs_National_View/12_local_external_ASNs_lastyear/files_origin/External_AFRINIC_ASNs_'+IXP+'.txt',
                        success: function() {
                            downloadURI('outputs_National_View/12_local_external_ASNs_lastyear/files_origin/External_AFRINIC_ASNs_'+IXP+'.txt','Last_year_at_'+IXP+'_External_AFRINIC.txt');
                        },  
                        error: function() {
                        
                        }
                    });
                    $.ajax({
                        type: 'HEAD',
                        url: 'outputs_National_View/12_local_external_ASNs_lastyear/files_origin/Local_AFRINIC_ASNs_'+IXP+'.txt',
                        success: function() {
                            downloadURI('outputs_National_View/12_local_external_ASNs_lastyear/files_origin/Local_AFRINIC_ASNs_'+IXP+'.txt','Last_year_at_'+IXP+'_Local_AFRINIC.txt');
                        },  
                        error: function() {
                        
                        }
                    });
                    $.ajax({
                        type: 'HEAD',
                        url: 'outputs_National_View/12_local_external_ASNs_lastyear/files_origin/Private_ASNs_'+IXP+'.txt',
                        success: function() {
                            downloadURI('outputs_National_View/12_local_external_ASNs_lastyear/files_origin/Private_ASNs_'+IXP+'.txt','Last_year_at_'+IXP+'_Private.txt');
                        },  
                        error: function() {
                        
                        }
                    })
                    $.ajax({
                        type: 'HEAD',
                        url: 'outputs_National_View/12_local_external_ASNs_lastyear/files_origin/Reserved_ASNs_'+IXP+'.txt',
                        success: function() {
                            downloadURI('outputs_National_View/12_local_external_ASNs_lastyear/files_origin/Reserved_ASNs_'+IXP+'.txt','Last_year_at_'+IXP+'_Reserved.txt');
                        },  
                        error: function() {
                        
                        }
                    })
                }
                
            }

            function descarga2(){
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
                        url: 'outputs_National_View/12_local_external_ASNs_multiyear/files_origin/APNIC_ASNs_'+IXP+'.txt',
                        success: function() {
                            downloadURI('outputs_National_View/12_local_external_ASNs_multiyear/files_origin/APNIC_ASNs_'+IXP+'.txt','Multiyear_at_'+IXP+'_APNIC.txt');
                        },  
                        error: function() {
                        
                        }
                    });
                    $.ajax({
                        type: 'HEAD',
                        url: 'outputs_National_View/12_local_external_ASNs_multiyear/files_origin/RIPE_ASNs_'+IXP+'.txt',
                        success: function() {
                            downloadURI('outputs_National_View/12_local_external_ASNs_multiyear/files_origin/RIPE_ASNs_'+IXP+'.txt','Multiyear_at_'+IXP+'_RIPE.txt');
                        },  
                        error: function() {
                        
                        }
                    });
                    $.ajax({
                        type: 'HEAD',
                        url: 'outputs_National_View/12_local_external_ASNs_multiyear/files_origin/ARIN_ASNs_'+IXP+'.txt',
                        success: function() {
                            downloadURI('outputs_National_View/12_local_external_ASNs_multiyear/files_origin/ARIN_ASNs_'+IXP+'.txt','Multiyear_at_'+IXP+'_ARIN.txt');
                        },  
                        error: function() {
                        
                        }
                    });
                    $.ajax({
                        type: 'HEAD',
                        url: 'outputs_National_View/12_local_external_ASNs_multiyear/files_origin/LACNIC_ASNs_'+IXP+'.txt',
                        success: function() {
                            downloadURI('outputs_National_View/12_local_external_ASNs_multiyear/files_origin/LACNIC_ASNs_'+IXP+'.txt','Multiyear_at_'+IXP+'_LACNIC.txt');
                        },  
                        error: function() {
                        
                        }
                    });
                    $.ajax({
                        type: 'HEAD',
                        url: 'outputs_National_View/12_local_external_ASNs_multiyear/files_origin/External_AFRINIC_ASNs_'+IXP+'.txt',
                        success: function() {
                            downloadURI('outputs_National_View/12_local_external_ASNs_multiyear/files_origin/External_AFRINIC_ASNs_'+IXP+'.txt','Multiyear_at_'+IXP+'_External_AFRINIC.txt');
                        },  
                        error: function() {
                        
                        }
                    });
                    $.ajax({
                        type: 'HEAD',
                        url: 'outputs_National_View/12_local_external_ASNs_multiyear/files_origin/Local_AFRINIC_ASNs_'+IXP+'.txt',
                        success: function() {
                            downloadURI('outputs_National_View/12_local_external_ASNs_multiyear/files_origin/Local_AFRINIC_ASNs_'+IXP+'.txt','Multiyear_at_'+IXP+'_Local_AFRINIC.txt');
                        },  
                        error: function() {
                        
                        }
                    });
                    $.ajax({
                        type: 'HEAD',
                        url: 'outputs_National_View/12_local_external_ASNs_multiyear/files_origin/Private_ASNs_'+IXP+'.txt',
                        success: function() {
                            downloadURI('outputs_National_View/12_local_external_ASNs_multiyear/files_origin/Private_ASNs_'+IXP+'.txt','Multiyear_at_'+IXP+'_Private.txt');
                        },  
                        error: function() {
                        
                        }
                    })
                    $.ajax({
                        type: 'HEAD',
                        url: 'outputs_National_View/12_local_external_ASNs_multiyear/files_origin/Reserved_ASNs_'+IXP+'.txt',
                        success: function() {
                            downloadURI('outputs_National_View/12_local_external_ASNs_multiyear/files_origin/Reserved_ASNs_'+IXP+'.txt','Multiyear_at_'+IXP+'_Reserved.txt');
                        },  
                        error: function() {
                        
                        }
                    })
                
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
            <div id ="select">
                <select name="selectIXP" id='selectIXP' onFocus='chargeList();' onClick='paint()'>
                    <option><b>Select Country:</b></option>
                </select>
            </div>
            <div>
                <div id="parrafos">
                    <p class ="titulo" id="titulo1">Distribution of non-local ASNs at CC</p>     
                    <p id="subtitulo">Per month over the last year</p>
                </div>
                <div id="originASNs" style="width: 100px; height: 300px;"></div>
                <div id= "botonDescarga">
                   <img onclick="javascript:descarga1();"id="enlaceDesgarga" src="images/dbutton.png" height="30">
                </div>
            </div>

            <div id="separador"></div>
            <div id="parrafos">
                <p class ="titulo" id="titulo2">Distribution of non-local ASNs at CC</p>     
                <p id="subtitulo">Per year over the historical Data (2005 up to now)</p>
            </div>
            <div id="lastYear" style="width: 1000px; height: 300px;"></div>
            <div id= "botonDescarga">
                   <img onclick="javascript:descarga2();" id="enlaceDesgarga" src="images/dbutton.png" height="30">
            </div>
        </div>
    </body>
</html>

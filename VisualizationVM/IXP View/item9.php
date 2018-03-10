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

            
            $lastYearASNs = array();
            for ($i=0; $i < count($listIXP); $i++) {
                if (file_exists('outputs/1_Number_prefixes_visibles_at_an_IXP_multiyear_lastyear/LastYear__number_visible_prefixes_at_IXP_with_slash_'.$listIXP[$i][0].'.txt') == 0) {
                    $file = fopen('outputs/1_Number_prefixes_visibles_at_an_IXP_multiyear_lastyear/LastYear__number_visible_prefixes_at_IXP_with_slash_'.$listIXP[$i][0].'.txt', "w");
                    fwrite($file, "" . PHP_EOL);
                    fclose($file);
                }
                $fileOpen = fopen('outputs/1_Number_prefixes_visibles_at_an_IXP_multiyear_lastyear/LastYear__number_visible_prefixes_at_IXP_with_slash_'.$listIXP[$i][0].'.txt','r');
                if (!$fileOpen){
                    echo 'ERROR: No ha sido posible abrir el archivo '.$listIXP[$i][0].'. Revisa su nombre y sus permisos.'; exit;
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
                        if (isset($informacion[$plantilla[$k][0]]["32"])) {
                            $plantilla[$k][1] = $informacion[$plantilla[$k][0]]["32"];
                        }
                        if (isset($informacion[$plantilla[$k][0]]["30"])) {
                            $plantilla[$k][2] = $informacion[$plantilla[$k][0]]["30"];
                        }
                        if (isset($informacion[$plantilla[$k][0]]["29"])) {
                            $plantilla[$k][3] = $informacion[$plantilla[$k][0]]["29"];
                        }
                        if (isset($informacion[$plantilla[$k][0]]["28"])) {
                            $plantilla[$k][4] = $informacion[$plantilla[$k][0]]["28"];
                        }
                        if (isset($informacion[$plantilla[$k][0]]["27"])) {
                            $plantilla[$k][5] = $informacion[$plantilla[$k][0]]["27"];
                        }
                        if (isset($informacion[$plantilla[$k][0]]["26"])) {
                            $plantilla[$k][6] = $informacion[$plantilla[$k][0]]["26"];
                        }
                        if (isset($informacion[$plantilla[$k][0]]["25"])) {
                            $plantilla[$k][7] = $informacion[$plantilla[$k][0]]["25"];
                        }
                        if (isset($informacion[$plantilla[$k][0]]["24"])) {
                            $plantilla[$k][8] = $informacion[$plantilla[$k][0]]["24"];
                        }
                    }
                } 
                $lastYearASNs[$i] = $plantilla;
            }

            $multiYearASNsv4 = array();
            for ($i=0; $i < count($listIXP); $i++) {
                if (file_exists('outputs/1_Number_prefixes_visibles_at_an_IXP_multiyear_lastyear/MultiYear__number_visible_prefixes_at_IXP_with_slash_'.$listIXP[$i][0].'.txt') == 0) {
                    $file = fopen('outputs/1_Number_prefixes_visibles_at_an_IXP_multiyear_lastyear/MultiYear__number_visible_prefixes_at_IXP_with_slash_'.$listIXP[$i][0].'.txt', "w");
                    fwrite($file, "" . PHP_EOL);
                    fclose($file);
                } 
                $fileOpen = fopen('outputs/1_Number_prefixes_visibles_at_an_IXP_multiyear_lastyear/MultiYear__number_visible_prefixes_at_IXP_with_slash_'.$listIXP[$i][0].'.txt','r');
                if (!$fileOpen){
                    echo 'ERROR: No ha sido posible abrir elkjhkjh archivo '.$listIXP[$i][0].'. Revisa su nombre y sus permisos.'; exit;
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
                        if (isset($informacion[$plantilla[$k][0]]["32"])) {
                            $plantilla[$k][1] = $informacion[$plantilla[$k][0]]["32"];
                        }
                        if (isset($informacion[$plantilla[$k][0]]["30"])) {
                            $plantilla[$k][2] = $informacion[$plantilla[$k][0]]["30"];
                        }
                        if (isset($informacion[$plantilla[$k][0]]["29"])) {
                            $plantilla[$k][3] = $informacion[$plantilla[$k][0]]["29"];
                        }
                        if (isset($informacion[$plantilla[$k][0]]["28"])) {
                            $plantilla[$k][4] = $informacion[$plantilla[$k][0]]["28"];
                        }
                        if (isset($informacion[$plantilla[$k][0]]["27"])) {
                            $plantilla[$k][5] = $informacion[$plantilla[$k][0]]["27"];
                        }
                        if (isset($informacion[$plantilla[$k][0]]["26"])) {
                            $plantilla[$k][6] = $informacion[$plantilla[$k][0]]["26"];
                        }
                        if (isset($informacion[$plantilla[$k][0]]["25"])) {
                            $plantilla[$k][7] = $informacion[$plantilla[$k][0]]["25"];
                        }
                        if (isset($informacion[$plantilla[$k][0]]["24"])) {
                            $plantilla[$k][8] = $informacion[$plantilla[$k][0]]["24"];
                        }
                    }
                } 
                $multiYearASNs[$i] = $plantilla;
            
            }
        ?>
        <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
        <script type="text/javascript" src="//cdnjs.cloudflare.com/ajax/libs/jquery/2.0.3/jquery.min.js"></script>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
        <script type="text/javascript" src="https://www.google.com/jsapi"></script>
        <script type="text/javascript">

            google.charts.load('current', {packages: ['corechart', 'line']})
    
            var listIXP = (<?php echo json_encode($listIXP)?>);
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
                    setTimeout(function(){ 
                        drawChart(numero);
                        console.log('Arreglado')
                    }, 1000); 
                    
                }else{
                    drawChart(numero-1);
                    var titulo = document.getElementById("titulo1");
                    var titulo2 = document.getElementById("titulo2");
                    IXP = (seleccionado.value).split(",")[0];
                    console.log('dedd')
                    titulo.innerHTML = "Number of long prefix length announcements at "+IXP;
                    titulo2.innerHTML = "Number of long prefix length announcements at "+IXP;
                }
            }

            function drawChart(i) {
                /*.........................*/
                var data = new google.visualization.DataTable();
                data.addColumn('string', 'Months');
                data.addColumn('number', '/32');
                data.addColumn('number', '/30');
                data.addColumn('number', '/29');
                data.addColumn('number', '/28');
                data.addColumn('number', '/27');
                data.addColumn('number', '/26');
                data.addColumn('number', '/25');
                data.addColumn('number', '/24');

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
                        title: 'Number of prefixes',
                        textStyle:{fontName: 'Trebuchet MS'},
                        titleTextStyle:{fontName: 'Trebuchet MS'}},
                    legend: {position: 'top',textStyle:{fontName: 'Trebuchet MS'}},
                    tooltip: {textStyle:{fontName: 'Trebuchet MS'}},
                    isStacked: 'percent',
                    colors: ['blue', '#C44441', '#8CBC4F', '#7A5892', 'green', '#F48533', '#8BAAD1', 'yellow']
                };

                var chart = new google.visualization.LineChart(document.getElementById('originASNs'));
                chart.draw(data, options);

                 /*.........................*/
                var data = new google.visualization.DataTable();
                data.addColumn('string', 'Years');
                data.addColumn('number', '/32');
                data.addColumn('number', '/30');
                data.addColumn('number', '/29');
                data.addColumn('number', '/28');
                data.addColumn('number', '/27');
                data.addColumn('number', '/26');
                data.addColumn('number', '/25');
                data.addColumn('number', '/24');

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
                        title: 'Number of prefixes',
                        textStyle:{fontName: 'Trebuchet MS'},
                        titleTextStyle:{fontName: 'Trebuchet MS'}},
                    legend: {position: 'top',textStyle:{fontName: 'Trebuchet MS'}},
                    tooltip: {textStyle:{fontName: 'Trebuchet MS'}},
                    isStacked: 'percent',
                    colors: ['blue', '#C44441', '#8CBC4F', '#7A5892', 'green', '#F48533', '#8BAAD1', 'yellow']
                };

                var chart = new google.visualization.LineChart(document.getElementById('lastYear'));
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
                        url: 'outputs/1_Number_prefixes_visibles_at_an_IXP_multiyear_lastyear/Lastyear__list_visible_prefixes_at_IXP_'+IXP+'_with_slash_24.txt',
                        success: function() {
                            downloadURI('outputs/1_Number_prefixes_visibles_at_an_IXP_multiyear_lastyear/Lastyear__list_visible_prefixes_at_IXP_'+IXP+'_with_slash_24.txt','Lastyear__list_visible_prefixes_at_'+IXP+'_24.txt');
                        },  
                        error: function() {
                        
                        }
                    });
                    $.ajax({
                        type: 'HEAD',
                        url: 'outputs/1_Number_prefixes_visibles_at_an_IXP_multiyear_lastyear/Lastyear__list_visible_prefixes_at_IXP_'+IXP+'_with_slash_25.txt',
                        success: function() {
                            downloadURI('outputs/1_Number_prefixes_visibles_at_an_IXP_multiyear_lastyear/Lastyear__list_visible_prefixes_at_IXP_'+IXP+'_with_slash_25.txt','Lastyear__list_visible_prefixes_at_'+IXP+'_25.txt');
                        },  
                        error: function() {
                        
                        }
                    });
                    $.ajax({
                        type: 'HEAD',
                        url: 'outputs/1_Number_prefixes_visibles_at_an_IXP_multiyear_lastyear/Lastyear__list_visible_prefixes_at_IXP_'+IXP+'_with_slash_25.txt',
                        success: function() {
                            downloadURI('outputs/1_Number_prefixes_visibles_at_an_IXP_multiyear_lastyear/Lastyear__list_visible_prefixes_at_IXP_'+IXP+'_with_slash_26.txt','Lastyear__list_visible_prefixes_at_'+IXP+'_26.txt');
                        },  
                        error: function() {
                        
                        }
                    });
                    $.ajax({
                        type: 'HEAD',
                        url: 'outputs/1_Number_prefixes_visibles_at_an_IXP_multiyear_lastyear/Lastyear__list_visible_prefixes_at_IXP_'+IXP+'_with_slash_27.txt',
                        success: function() {
                            downloadURI('outputs/1_Number_prefixes_visibles_at_an_IXP_multiyear_lastyear/Lastyear__list_visible_prefixes_at_IXP_'+IXP+'_with_slash_27.txt','Lastyear__list_visible_prefixes_at_'+IXP+'_27.txt');
                        },  
                        error: function() {
                        
                        }
                    });
                    $.ajax({
                        type: 'HEAD',
                        url: 'outputs/1_Number_prefixes_visibles_at_an_IXP_multiyear_lastyear/Lastyear__list_visible_prefixes_at_IXP_'+IXP+'_with_slash_28.txt',
                        success: function() {
                            downloadURI('outputs/1_Number_prefixes_visibles_at_an_IXP_multiyear_lastyear/Lastyear__list_visible_prefixes_at_IXP_'+IXP+'_with_slash_28.txt','Lastyear__list_visible_prefixes_at_'+IXP+'_28.txt');
                        },  
                        error: function() {
                        
                        }
                    });
                    $.ajax({
                        type: 'HEAD',
                        url: 'outputs/1_Number_prefixes_visibles_at_an_IXP_multiyear_lastyear/Lastyear__list_visible_prefixes_at_IXP_'+IXP+'_with_slash_29.txt',
                        success: function() {
                            downloadURI('outputs/1_Number_prefixes_visibles_at_an_IXP_multiyear_lastyear/Lastyear__list_visible_prefixes_at_IXP_'+IXP+'_with_slash_29.txt','Lastyear__list_visible_prefixes_at_'+IXP+'_29.txt');
                        },  
                        error: function() {
                        
                        }
                    });
                    $.ajax({
                        type: 'HEAD',
                        url: 'outputs/1_Number_prefixes_visibles_at_an_IXP_multiyear_lastyear/Lastyear__list_visible_prefixes_at_IXP_'+IXP+'_with_slash_30.txt',
                        success: function() {
                            downloadURI('outputs/1_Number_prefixes_visibles_at_an_IXP_multiyear_lastyear/Lastyear__list_visible_prefixes_at_IXP_'+IXP+'_with_slash_30.txt','Lastyear__list_visible_prefixes_at_'+IXP+'_30.txt');
                        },  
                        error: function() {
                        
                        }
                    });
                    $.ajax({
                        type: 'HEAD',
                        url: 'outputs/1_Number_prefixes_visibles_at_an_IXP_multiyear_lastyear/Lastyear__list_visible_prefixes_at_IXP_'+IXP+'_with_slash_32.txt',
                        success: function() {
                            downloadURI('outputs/1_Number_prefixes_visibles_at_an_IXP_multiyear_lastyear/Lastyear__list_visible_prefixes_at_IXP_'+IXP+'_with_slash_32.txt','Lastyear__list_visible_prefixes_at_'+IXP+'_32.txt');
                        },  
                        error: function() {
                        
                        }
                    });
                    
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
                        url: 'outputs/1_Number_prefixes_visibles_at_an_IXP_multiyear_lastyear/Multiyear__list_visible_prefixes_at_IXP_'+IXP+'_with_slash_24.txt',
                        success: function() {
                            downloadURI('outputs/1_Number_prefixes_visibles_at_an_IXP_multiyear_lastyear/Multiyear__list_visible_prefixes_at_IXP_'+IXP+'_with_slash_24.txt','Multiyear__list_visible_prefixes_at_'+IXP+'_24.txt');
                        },  
                        error: function() {
                        
                        }
                    });
                    $.ajax({
                        type: 'HEAD',
                        url: 'outputs/1_Number_prefixes_visibles_at_an_IXP_multiyear_lastyear/Multiyear__list_visible_prefixes_at_IXP_'+IXP+'_with_slash_25.txt',
                        success: function() {
                            downloadURI('outputs/1_Number_prefixes_visibles_at_an_IXP_multiyear_lastyear/Multiyear__list_visible_prefixes_at_IXP_'+IXP+'_with_slash_25.txt','Multiyear__list_visible_prefixes_at_'+IXP+'_25.txt');
                        },  
                        error: function() {
                        
                        }
                    });
                    $.ajax({
                        type: 'HEAD',
                        url: 'outputs/1_Number_prefixes_visibles_at_an_IXP_multiyear_lastyear/Multiyear__list_visible_prefixes_at_IXP_'+IXP+'_with_slash_26.txt',
                        success: function() {
                            downloadURI('outputs/1_Number_prefixes_visibles_at_an_IXP_multiyear_lastyear/Multiyear__list_visible_prefixes_at_IXP_'+IXP+'_with_slash_26.txt','Multiyear__list_visible_prefixes_at_'+IXP+'_26.txt');
                        },  
                        error: function() {
                        
                        }
                    });
                    $.ajax({
                        type: 'HEAD',
                        url: 'outputs/1_Number_prefixes_visibles_at_an_IXP_multiyear_lastyear/Multiyear__list_visible_prefixes_at_IXP_'+IXP+'_with_slash_27.txt',
                        success: function() {
                            downloadURI('outputs/1_Number_prefixes_visibles_at_an_IXP_multiyear_lastyear/Multiyear__list_visible_prefixes_at_IXP_'+IXP+'_with_slash_27.txt','Multiyear__list_visible_prefixes_at_'+IXP+'_27.txt');
                        },  
                        error: function() {
                        
                        }
                    });
                    $.ajax({
                        type: 'HEAD',
                        url: 'outputs/1_Number_prefixes_visibles_at_an_IXP_multiyear_lastyear/Multiyear__list_visible_prefixes_at_IXP_'+IXP+'_with_slash_28.txt',
                        success: function() {
                            downloadURI('outputs/1_Number_prefixes_visibles_at_an_IXP_multiyear_lastyear/Multiyear__list_visible_prefixes_at_IXP_'+IXP+'_with_slash_28.txt','Multiyear__list_visible_prefixes_at_'+IXP+'_28.txt');
                        },  
                        error: function() {
                        
                        }
                    });
                    $.ajax({
                        type: 'HEAD',
                        url: 'outputs/1_Number_prefixes_visibles_at_an_IXP_multiyear_lastyear/Multiyear__list_visible_prefixes_at_IXP_'+IXP+'_with_slash_29.txt',
                        success: function() {
                            downloadURI('outputs/1_Number_prefixes_visibles_at_an_IXP_multiyear_lastyear/Multiyear__list_visible_prefixes_at_IXP_'+IXP+'_with_slash_29.txt','Multiyear__list_visible_prefixes_at_'+IXP+'_29.txt');
                        },  
                        error: function() {
                        
                        }
                    });
                    $.ajax({
                        type: 'HEAD',
                        url: 'outputs/1_Number_prefixes_visibles_at_an_IXP_multiyear_lastyear/Multiyear__list_visible_prefixes_at_IXP_'+IXP+'_with_slash_30.txt',
                        success: function() {
                            downloadURI('outputs/1_Number_prefixes_visibles_at_an_IXP_multiyear_lastyear/Multiyear__list_visible_prefixes_at_IXP_'+IXP+'_with_slash_30.txt','Multiyear__list_visible_prefixes_at_'+IXP+'_30.txt');
                        },  
                        error: function() {
                        
                        }
                    });
                    $.ajax({
                        type: 'HEAD',
                        url: 'outputs/1_Number_prefixes_visibles_at_an_IXP_multiyear_lastyear/Multiyear__list_visible_prefixes_at_IXP_'+IXP+'_with_slash_32.txt',
                        success: function() {
                            downloadURI('outputs/1_Number_prefixes_visibles_at_an_IXP_multiyear_lastyear/Multiyear__list_visible_prefixes_at_IXP_'+IXP+'_with_slash_32.txt','Multiyear__list_visible_prefixes_at_'+IXP+'_32.txt');
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
                margin-top: 20px;
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
                    <p class ="titulo" id="titulo1">Number of long prefix length announcements at IXP</p>     
                    <p id="subtitulo">Per month over the last year</p>
                </div>
                <div id="originASNs" style="width: 100px; height: 300px;"></div>
                <div id= "botonDescarga">
                   <img onclick="javascript:descarga1();"id="enlaceDesgarga" src="images/dbutton.png" height="30">
                </div>
            </div>

            <div id="separador"></div>
            <div id="parrafos">
                <p class ="titulo" id="titulo2">Number of long prefix length announcements at IXP</p>     
                <p id="subtitulo">Per year over the historical Data (2005 up to now)</p>
            </div>
            <div id="lastYear" style="width: 1000px; height: 300px;"></div>
            <div id= "botonDescarga">
                   <img onclick="javascript:descarga2();" id="enlaceDesgarga" src="images/dbutton.png" height="30">
            </div>
        </div>
    </body>
</html>

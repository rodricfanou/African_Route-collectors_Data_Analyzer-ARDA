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


             $percentage1 = array();

            //Txt in to an array
            $fileOpen = fopen('outputs/3_percentage_Origin_ASNs_by_country_assignment_lastmonth/1_percentage_of_allocated_ASNs_seen_as_origin_ASNs_at_an_IXP.txt','r');
            if (!$fileOpen){
                echo 'ERROR: No ha sido posible abrir el arsdchivo. Revisa su nombre y sus permisos.'; exit;
            }

            $index = 0; // contador de líneas
            while (!feof($fileOpen)) { // loop hasta que se llegue al final del archivo
                $index++;
                $line = trim(fgets($fileOpen)); // guardamos toda la línea en $line como un string
                $percentage1[$index] = explode(";",$line);
                $fileOpen++; // necesitamos llevar el puntero del archivo a la siguiente línea
            }

            $percentage12 = array();
            for ($i=2; $i < count($percentage1); $i++) { 
                $percentage12[$i-2][0] = $percentage1[$i][0];
                $percentage12[$i-2][1] = intval($percentage1[$i][2]);
                $percentage12[$i-2][2] = intval($percentage1[$i][3])-intval($percentage1[$i][2]);
            }
            $percentage1 = $percentage12;

             //Per region
            $percentage1perRegion = array();
            for ($i=0; $i < count($listIXP); $i++) {
                if (file_exists('outputs/3_percentage_Origin_ASNs_by_country_assignment_lastmonth/Percentage_Origin_ASNs_by_region_'.$listIXP[$i][0].'.txt') == 0) {
                    $file = fopen('outputs/3_percentage_Origin_ASNs_by_country_assignment_lastmonth/Percentage_Origin_ASNs_by_region_'.$listIXP[$i][0].'.txt', "w");
                    fwrite($file, "" . PHP_EOL);
                    fclose($file);
                } 

                $list1 = array();
           
                $fileOpen = fopen('outputs/3_percentage_Origin_ASNs_by_country_assignment_lastmonth/Percentage_Origin_ASNs_by_region_'.$listIXP[$i][0].'.txt','r');
                $numero = count(file('outputs/3_percentage_Origin_ASNs_by_country_assignment_lastmonth//Percentage_Origin_ASNs_by_region_'.$listIXP[$i][0].'.txt'));
                if (!$fileOpen){
                    echo 'ERROR: No ha sido posible abrir el archxcvivo. Revisa su nombre y sus permisos.'; exit;
                }

                $index = 0; // contador de líneas
                while (!feof($fileOpen)) { // loop hasta que se llegue al final del archivo
                  $line = trim(fgets($fileOpen)); // guardamos toda la línea en $line como un string
                  $pos = strpos($line, '#');
                  if($pos === false){
                        $list1[$index] = explode(";",$line);
                        $fileOpen++; // necesitamos llevar el puntero del archivo a la siguiente línea
                        $index++;
                    }
                }

                $list12 = array();

                for ($j=0; $j < count($list1); $j++) { 
                 $list12[$j][0] = $list1[$j][0];
                 $list12[$j][1] = floatval($list1[$j][1]);
                }
                $percentage1perRegion[$i] = $list12;
            }

            //Per country
            $percentage1perCountry = array();
            for ($i=0; $i < count($listIXP); $i++) { 

                if (file_exists('outputs/3_percentage_Origin_ASNs_by_country_assignment_lastmonth/Percentage_Origin_ASNs_by_country_assignment_'.$listIXP[$i][0].'.txt') == 0) {
                    $file = fopen('outputs/3_percentage_Origin_ASNs_by_country_assignment_lastmonth/Percentage_Origin_ASNs_by_country_assignment_'.$listIXP[$i][0].'.txt', "w");
                    fwrite($file, "" . PHP_EOL);
                    fclose($file);
                } 

                $list1 = array();
               
                $fileOpen = fopen('outputs/3_percentage_Origin_ASNs_by_country_assignment_lastmonth/Percentage_Origin_ASNs_by_country_assignment_'.$listIXP[$i][0].'.txt','r');
                $numero = count(file('outputs/3_percentage_Origin_ASNs_by_country_assignment_lastmonth/Percentage_Origin_ASNs_by_country_assignment_'.$listIXP[$i][0].'.txt'));
                if (!$fileOpen){
                    echo 'ERROR: No ha sido posible abrir elbf archivosdas. Revisa su nombre y sus permisos.'; exit;
                }

                $index = 0; // contador de líneas
                while (!feof($fileOpen)) { // loop hasta que se llegue al final del archivo
                    $index++;
                    $line = trim(fgets($fileOpen)); // guardamos toda la línea en $line como un string
                    $list1[$index] = explode(";",$line);
                    $fileOpen++; // necesitamos llevar el puntero del archivo a la siguiente línea
                }

               

                //Txt in to an array
                $fileOpen = fopen('outputs/3_percentage_Origin_ASNs_by_country_assignment_lastmonth/Number_ASNs_assigned_by_Afrinic.txt','r');
                if (!$fileOpen){
                    echo 'ERROR: No ha sido posible abrir el archweweivo. Revisa su nombre y sus permisos.'; exit;
                }

                $index = 0; // contador de líneas
                while (!feof($fileOpen)) { // loop hasta que se llegue al final del archivo
                    $line = trim(fgets($fileOpen)); // guardamos toda la línea en $line como un string
                    $aux = explode(";",$line);
                    $number_AFRINIC[$aux[0]] = $aux[1]; 
                    $fileOpen++; // necesitamos llevar el puntero del archivo a la siguiente línea
                    $index++;
                }

                $list12 = array();

                for ($j=1; $j < $numero+1 ; $j++) { 
                    $list12[$j-1][0] = $list1[$j][0];
                    $list12[$j-1][1] = floatval($list1[$j][2]);
                    $list12[$j-1][2] = '<b>'.$list1[$j][0].' ('.$list1[$j][1].')</b>'.
                    '<br>Number of ASNs visible at '.$listIXP[$i][0].': <b>'.number_format(floatval($list1[$j][3])).'</b>'.
                    '<br>Number of ASNs assigned to '.$list1[$j][0].' visible at '.$listIXP[$i][0].': <b>'.$list1[$j][2].' ('.(number_format(floatval($list1[$j][4]),2)).'%)</b>'.
                    '<br>% ASNs assigned to '.$list1[$j][0].' visible at '.$listIXP[$i][0].': <b>'.(number_format(floatval($list1[$j][6]),2)).'%</b>'. 
                    '<br>Number of ASNs assigned to '.$list1[$j][0].' by AFRINIC: <b>'.$number_AFRINIC[$list1[$j][0]].'</b>';
                    //$list12[$j-1][3] = floatval($list1[$j][4]);
                    /* $list12[$j-1][2] = '<b>'.$list1[$j][0].' ('.$list1[$j][1].')</b>'.
                    '<br># ASNs assigned to '.$list1[$j][0].' visible at '.$listIXP[$i][1].': <b>'.$list1[$j][2].'</b>'.
                    '<br>% ASNs visible at '.$listIXP[$i][1].' corresponding to '.$list1[$j][0].' ASNs: <b>'.(number_format(floatval($list1[$j][3]),2)).'</b>'.
                    '<br>% ASNs assigned to '.$list1[$j][0].' visible at '.$listIXP[$i][1].' ASNs: <b>'.(number_format(floatval($list1[$j][4]),2)).'</b>';
                    //$list12[$j-1][3] = floatval($list1[$j][4]);*/
                }
                
                $percentage1perCountry[$i] = $list12;
            }

            $lastYearASNs = array();
            for ($i=0; $i < count($listIXP); $i++) {
                if (file_exists('outputs/3_Number_percentage_Origin_by_country_assignment_lastyear/LastYear__local_vs_External_ASNs_to_the_country_hosting_IXP_visible_at_IXP_'.$listIXP[$i][0].'.txt') == 0) {
                    $file = fopen('outputs/3_Number_percentage_Origin_by_country_assignment_lastyear/LastYear__local_vs_External_ASNs_to_the_country_hosting_IXP_visible_at_IXP_'.$listIXP[$i][0].'.txt', "w");
                    fwrite($file, "" . PHP_EOL);
                    fclose($file);
                }
                $fileOpen = fopen('outputs/3_Number_percentage_Origin_by_country_assignment_lastyear/LastYear__local_vs_External_ASNs_to_the_country_hosting_IXP_visible_at_IXP_'.$listIXP[$i][0].'.txt','r');
                if (!$fileOpen){
                    echo 'ERROR: No ha sido posible abrir el asdasdasdarchivo'.$listIXP[$i][0].'. Revisa su nombre y sus permisos.'; exit;
                }

                for ($z = 1; $z <= 12; $z++) {
                    $months[] = date("m-Y", strtotime( date( 'Y-m-01' )." -$z months"));
                }

                $prueba = array();
                for ($z=0; $z < count($months); $z++) {
                    $aux = explode("-",$months[$z]);
                    $aux[0] = (string)intval($aux[0]); 
                    $prueba[$z] = $aux[0].'-'.$aux[1].';0;0';
                }

                $prueba = array_reverse($prueba);
                $month = intval(date("m"));
                $plantilla = array();
                for ($k=0; $k < 12; $k++) { 
                    $plantilla[$k] = explode(";",$prueba[$k]);
                }

                $list =  array();
                $index = 0; // contador de líneas
                while (!feof($fileOpen)) { // loop hasta que se llegue al final del archivo
                    $line = trim(fgets($fileOpen)); // guardamos toda la línea en $line como un string
                    $list[$index] = explode(";",$line);
                    $fileOpen++; // necesitamos llevar el puntero del archivo a la siguiente línea
                    $index++;
                }

                for ($k=0; $k < count($plantilla); $k++) { 
                    for ($j=0; $j < count($list); $j++) { 
                        if (strcmp(trim($plantilla[$k][0]), trim($list[$j][2])) == 0) {
                            $plantilla[$k][1] = intval($list[$j][4]) - intval($list[$j][3]);
                            $plantilla[$k][2] = intval($list[$j][3]);
                        }
                    }
                } 
                $lastYearASNs[$i] = $plantilla;
            }

            $multiYearASNs = array();
            for ($i=0; $i < count($listIXP); $i++) {
                if (file_exists('outputs/3_Number_percentage_Origin_by_country_assignment_lastyear/MultiYear__local_vs_External_ASNs_to_the_country_hosting_IXP_visible_at_IXP_'.$listIXP[$i][0].'.txt') == 0) {
                    $file = fopen('outputs/3_Number_percentage_Origin_by_country_assignment_lastyear/MultiYear__local_vs_External_ASNs_to_the_country_hosting_IXP_visible_at_IXP_'.$listIXP[$i][0].'.txt', "w");
                    fwrite($file, "" . PHP_EOL);
                    fclose($file);
                }
                $fileOpen = fopen('outputs/3_Number_percentage_Origin_by_country_assignment_lastyear/MultiYear__local_vs_External_ASNs_to_the_country_hosting_IXP_visible_at_IXP_'.$listIXP[$i][0].'.txt','r');
                if (!$fileOpen){
                    echo 'ERROR: No ha sido jljlkjlkjposible abrir el archivo'.$listIXP[$i][0].'. Revisa su nombre y sus permisos.'; exit;
                }

                $list = array();
                $index = 0; // contador de líneas
                while (!feof($fileOpen)) { // loop hasta que se llegue al final del archivo
                    $line = trim(fgets($fileOpen)); // guardamos toda la línea en $line como un string
                    $list[$index] = explode(";",$line);
                    $fileOpen++; // necesitamos llevar el puntero del archivo a la siguiente línea
                    $index++;
                }

                $years = array();
                for ($j = 0; $j <= intval(date("Y"))-2005; $j++) {
                        $years[$j][0] = (string)($j+2005);
                        $years[$j][1] = 0;
                        $years[$j][2] = 0;
                }
                
                for ($j=0; $j <count($years); $j++) { 
                    for ($k=0; $k <count($list) ; $k++) { 
                        if(strcmp($years[$j][0], $list[$k][2]) == 0){
                            $years[$j][1] = intval($list[$k][4]);
                            $years[$j][2] = intval($list[$k][3]);
                        }
                    }
                }
                $list = $years;
                $multiYearASNs[$i] = $list;
            }

            ?>

        <script type="text/javascript" src="//cdnjs.cloudflare.com/ajax/libs/jquery/2.0.3/jquery.min.js"></script>
        <script type="text/javascript" src="https://www.google.com/jsapi"></script>
        <script type="text/javascript">
     
            google.load("visualization", "1", {packages:["geochart","corechart"]});
            google.setOnLoadCallback(init);

            var listIXP = (<?php echo json_encode($listIXP)?>);
            var number_AFRINIC = (<?php echo json_encode($number_AFRINIC)?>);
            var percentage1 = (<?php echo json_encode($percentage1)?>);
            var percentage1perRegion = (<?php echo json_encode($percentage1perRegion)?>);
            var percentage1perCountry = (<?php echo json_encode($percentage1perCountry)?>);
            var porcentaje1 = [];
            var multiYearASNs = (<?php echo json_encode($multiYearASNs)?>);
            var lastYearASNs = (<?php echo json_encode($lastYearASNs)?>);
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

            for (var i = 0; i < lastYearASNs.length; i++) {
                for (var j = 0; j < lastYearASNs[i].length; j++) {
                    aux = lastYearASNs[i][j][0].split("-");
                    aux[0] = month[parseInt(aux[0])-1];
                    lastYearASNs[i][j][0] = aux[0]+" "+aux[1]
                    lastYearASNs[i][j][1] = parseInt(lastYearASNs[i][j][1]);
                    lastYearASNs[i][j][2] = parseInt(lastYearASNs[i][j][2]);
                };
            };



            function init(){
                document.getElementById("titulo1").innerHTML = "Percentage of ASNs allocated to "+listIXP[0][1]+" visible or not at "+listIXP[0][0];
                document.getElementById("titulo2").innerHTML = "Percentage of ASNs assigned by each RIR visible at "+listIXP[0][0];
                document.getElementById("titulo3").innerHTML = "Percentage of ASNs assigned to each country by its corresponding RIR";
                document.getElementById("titulo4").innerHTML = "Local vs External ASNs visible at "+listIXP[0][0];
                document.getElementById("titulo5").innerHTML = "Local vs External ASNs visible at "+listIXP[0][0];
                document.getElementById("subtitulo3").innerHTML = "Visible at "+listIXP[0][0]+" as Origin ASNs over the last month";
                formatoCorrecto();
                drawChart(0);
                drawRegionsMap(0);
                console.log("hola")
            }

            function paint(){
                var seleccionado = document.getElementById("selectIXP");
                var numero = seleccionado.selectedIndex;
                if (numero == 0) {
                    numero = 1;
                };
                var valor = seleccionado.value;
                document.getElementById("titulo1").innerHTML = "Percentage of ASNs allocated to "+listIXP[numero-1][1]+" visible or not at "+listIXP[numero-1][0];
                document.getElementById("titulo2").innerHTML = "Percentage of ASNs assigned by each RIR visible at "+listIXP[numero-1][0];
                document.getElementById("titulo4").innerHTML = "Local vs External ASNs visible at "+listIXP[numero-1][0];
                document.getElementById("titulo5").innerHTML = "Local vs External ASNs visible at "+listIXP[numero-1][0];
                document.getElementById("subtitulo3").innerHTML = "Visible at "+listIXP[numero-1][0]+" as Origin ASNs over the last month";
                drawChart(numero-1);
                drawRegionsMap(numero-1);
            }
     
            function drawChart(i) {
       
                var data = new google.visualization.DataTable();

                data.addColumn('string', 'Country');
                data.addColumn('number', 'Percentage');
                data.addRows(porcentaje1[i]);

                var options = {
                  'title':'Origin ASNs',
                  is3D: false,
                  fontName: 'Trebuchet MS',
                  sliceVisibilityThreshold: .000000000000000000002,
                  colors: ['#53A8FB', '#F1CA3A']
                };

                var chart = new google.visualization.PieChart(document.getElementById('piechart11'));
                google.visualization.events.addListener(chart, 'select', selectHandler);
                chart.draw(data, options);
                function selectHandler() {
                    var selectedItem = chart.getSelection()[0];
                    console.log(selectedItem);
                    if (selectedItem.row == 0){
                        if (confirm("Do you want to download this file?") == true) {
                            downloadURI("outputs/3_percentage_Origin_ASNs_by_country_assignment_lastmonth/Origin_ASNs_assigned_to_country_seen_at_"+listIXP[i][0]+".txt","Origin_ASNs_assigned_to_country_seen_at_"+listIXP[i][0]+".txt"); 
                        }
                    };
                    if (selectedItem.row == 1) {
                        if (confirm("Do you want to download this file?") == true) {
                            downloadURI("outputs/3_percentage_Origin_ASNs_by_country_assignment_lastmonth/Origin_ASNs_assigned_to_country_Not_seen_at_"+listIXP[i][0]+".txt","Origin_ASNs_assigned_to_country_Not_seen_at_"+listIXP[i][0]+".txt");
                        }
                    };
                };

                /*----------------------------------------------------------------------------*/

                var data2 = new google.visualization.DataTable();
        
                data2.addColumn('string', 'Region');
                data2.addColumn('number', 'Percentage');
                data2.addRows(percentage1perRegion[i]);

                var options2 = {
                    'title':'Origin ASNs',
                    is3D: false,
                    sliceVisibilityThreshold: .000000000000000000002,
                    fontName: 'Trebuchet MS'
                };

                var chart2 = new google.visualization.PieChart(document.getElementById('piechart21'));
                google.visualization.events.addListener(chart2, 'select', selectHandler2);
                chart2.draw(data2, options2);
                 function selectHandler2() {
                    var selectedItem = chart2.getSelection()[0];
                    console.log(selectedItem);
                    if (selectedItem) {
                        var value = data2.getValue(selectedItem.row,0);
                        var find = ' ';
                        var re = new RegExp(find, 'g');
                        value = value.replace(re, "_");
                    }
                    if (confirm("Do you want to download this file?") == true) {
                        downloadURI('outputs/3_percentage_Origin_ASNs_by_country_assignment_lastmonth/files_origin/'+value+'_'+listIXP[i][0]+'.txt',value+'_'+listIXP[i][0]+'.txt');
                    }
                    
                }

                /*.........................*/
                var data = new google.visualization.DataTable();
                data.addColumn('string', 'Years');
                data.addColumn('number', '# External');
                data.addColumn('number', '# Local');

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
                    legend: {textStyle:{fontName: 'Trebuchet MS'}},
                    tooltip: {textStyle:{fontName: 'Trebuchet MS'}},
                    colors: ['#53A8FB', '#F1CA3A'],
                };

                var chart = new google.visualization.SteppedAreaChart(document.getElementById('multiYear'));
                chart.draw(data, options);

                /*.........................*/
                var data = new google.visualization.DataTable();
                data.addColumn('string', 'Months');
                data.addColumn('number', '# External');
                data.addColumn('number', '# Local');

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
                    legend: {textStyle:{fontName: 'Trebuchet MS'}},
                    tooltip: {textStyle:{fontName: 'Trebuchet MS'}},
                    colors: ['#53A8FB', '#F1CA3A'],
                };

                var chart = new google.visualization.SteppedAreaChart(document.getElementById('lastYear'));
                chart.draw(data, options);
            }

            function drawRegionsMap(i) {
            
                var data = new google.visualization.DataTable();

                data.addColumn('string', 'Country');
                data.addColumn('number', '# ASNs visible at '+listIXP[i][0]);
                data.addColumn({type:'string', role: 'tooltip', p:{html:true, showTitle:false}});
                //data.addColumn('number', 'Percentage 2');

                data.addRows(percentage1perCountry[i]);

                var options = {title: 'Percentage per country',
                    datalessRegionColor: 'white',
                    fontName: 'Trebuchet MS',
                    enableRegionInteractivity: 'true',
                    tooltip : {textStyle: {color: '#666'}, showColorCode: true, isHtml: true},
                    colorAxis: {colors: ['#00853f', 'black', '#e31b23']}
                };

                var chart = new google.visualization.GeoChart(document.getElementById('regions_div'));
                /*
                google.visualization.events.addListener(chart, 'select', selectHandler);
                function selectHandler() {
                var selectedItem = chart.getSelection()[0]
                    var value = data.getValue(selectedItem.row,0);
                    alert('The user will download a file from ' + value+' at IXP: '+listIXP[i]+' '+AvsO);
                   
                };*/

                chart.draw(data, { tooltip: {
                    isHtml: true
                }});
            }

            function formatoCorrecto(){
                auxiliar1 = [[,],[,]];
                for (var i = 0; i < listIXP.length; i++) {
                    for (var j = 0; j < percentage1.length; j++) {
                        if(percentage1[j][0].trim() == listIXP[i][0].trim()){
                            auxiliar1[0][0] = 'Number of visible \n local ASNs';
                            auxiliar1[0][1] = percentage1[j][1];
                            auxiliar1[1][0] = 'Number of local \n ASNs not seen';
                            auxiliar1[1][1] = percentage1[j][2];
                            porcentaje1.push(auxiliar1);
                            j=300;
                        }
                        auxiliar1 = [[,],[,]];
                    };
                };
            }

            function downloadURI(uri,name) {
                var link = document.createElement("a");
                link.download = name;
                link.href = uri;
                link.click();
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

            function descarga3(){
                console.log("adddd")
                var seleccionado = document.getElementById("selectIXP");
                var numero = seleccionado.selectedIndex;
                if (numero == 0) {
                    alert("Select an IXP");
                }else{
                    IXP = (seleccionado.value).split(",")[0];
                    console.log (IXP)
                    downloadURI('outputs/3_Number_percentage_Origin_by_country_assignment_lastyear/MultiYear__list_visible_ASNs_at_IXP_'+IXP+'.txt',seleccionado.value+'.txt');
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
                    downloadURI('outputs/3_Number_percentage_Origin_by_country_assignment_lastyear/LastYear__list_visible_ASNs_at_IXP_'+IXP+'.txt',seleccionado.value+'.txt');
                }
                
            }

            $(window).resize(function () {
                resize();
            });

            $(document).ready(function(){
                resize();
            });

            var designWidth = 1100;
            console.log(designWidth)

            function resize() {
                var w = $(window).width();
                var zoom = parseInt(w / designWidth * 100).toString() + "%";
                $("#content").css("zoom", zoom);
            }

        </script>
        <style type="text/css">
        #select{
            margin: 10px;
            font-family: 'Trebuchet MS';
            margin-left: 465px
        }
        #parrafos{
            line-height: 1px;
        }
        #parrafos2{
            line-height: 1px;
            margin-left: 100px;
        }

        .titulo{
            font-size: 17depx;
            font-family: 'Trebuchet MS';
            font-weight: 400;
            color: #757575;
        }
        #multiyear {
                margin-left: 40px;
            }
            #lastyear {
                margin-left: 40px;
            }


        #subtitulo{
            font-size: 14px;
            font-family: 'Trebuchet MS';
            color: #BDBDBD;
        }
        #subtitulo3{
            font-size: 14px;
            font-family: 'Trebuchet MS';
            color: #BDBDBD;
        }
        #seleccionASNs{
            all: none;
        }
        #separador {
            margin-top: 15px;
        }
        #separador2 {
            margin-top: 50px;
        }
        #botonDescarga{
                top: 100px;
                margin-left: 900px;
                font-size: 12px;
                font-family: 'Trebuchet MS'
            }
     .google-visualization-tooltip{
    
    }
    .google-visualization-tooltip-item
    {
      font-family: 'Trebuchet MS';
    }
    .google-visualization-tooltip-item-list .google-visualization-tooltip-item:first-child 
    {
        display: none; 
    }  
    }
  
    </style>
    </head>
    <body>
        <div id="content">
            <div id ="select">
                <select name="selectIXP" id='selectIXP' onFocus='chargeList();' onClick='paint()'>
                    <option>Select IXP :</option>
                </select>
    
            </div>

            <div style="width: 1300px; height: 375px; margin-left:0px;">
                <div id="primero" style="width: 550px; height: 400px; margin-left:30px; display: inline-block;">
                    <div id="parrafos">
                        <p class ="titulo" id="titulo1"></p>     
                        <p id="subtitulo">As Origin ASNs over the last month</p>
                    </div>
                    <div id="piechart11" style="width: 550px; height: 350px; float: left;"></div>
                </div>
                <div id="segundo" style="width: 550px; height: 400px; margin-left:30px; display: inline-block;">
                    <div id="parrafos">
                        <p class="titulo" id="titulo2">Percentage of ASNs by region assignment</p>     
                        <p id="subtitulo">As Origin ASNs over the last month</p>
                    </div>
                    <div id="piechart21" style="width: 550px; height: 350px; float: left;"></div>
                </div>   
            </div>
            <div id="separador"></div>
            <div style="width: 1100px; height: 60px; margin-left:30px">
                <div id="parrafos" style="float:left;">
                    <p class="titulo" id="titulo3">Percentage of ASNs by country assignment</p>     
                    <p id="subtitulo3" >As Origin ASNs over the last month</p>
                </div>
                <div style="float:left;  margin-left: 500px;"></div>
            </div>
            <div id="regions_div" style="width: 1000px;margin-left:30px"></div>
            <div id="separador2"></div>
            <div id="parrafos2">
                <p class ="titulo" id="titulo5">Local vs External ASNs visible at IXP</p>     
                <p id="subtitulo">Per month over the last year</p>
            </div>
            <div id="lastYear" style="width: 1000px; height: 300px;"></div>
            <div id= "botonDescarga">
                   <img onclick="javascript:descarga2();" id="enlaceDesgarga" src="images/dbutton.png" height="30">
            </div>

            <div id="separador2"></div>
            <div id="parrafos2">
                <p class ="titulo" id="titulo4">Local vs External ASNs visible at IXP</p>     
                <p id="subtitulo">Per year over the historical Data (2005 up to now)</p>
            </div>
            <div id="multiYear" style="width: 1000px; height: 300px;"></div>
            <div id= "botonDescarga">
                   <img onclick="javascript:descarga3();" id="enlaceDesgarga" src="images/dbutton.png" height="30">
            </div>
            
        </div>
  </body>
</html>
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

            //Origin
            $lastMonthASNs = array();
            for ($i=0; $i < count($listCC); $i++) {
                if (file_exists('outputs_National_View/1_Number_ASNs_origin_in_more_than_1_IXP_per_country_lastmonth/LastMonth__number_visible_origin_ASNs_in_more_than_1_IXP_of_'.$listCC[$i][0].'.txt') == 0) {
                    $file = fopen('outputs_National_View/1_Number_ASNs_origin_in_more_than_1_IXP_per_country_lastmonth/LastMonth__number_visible_origin_ASNs_in_more_than_1_IXP_of_'.$listCC[$i][0].'.txt', "w");
                    fwrite($file, "" . PHP_EOL);
                    fclose($file);
                }
                $fileOpen = fopen('outputs_National_View/1_Number_ASNs_origin_in_more_than_1_IXP_per_country_lastmonth/LastMonth__number_visible_origin_ASNs_in_more_than_1_IXP_of_'.$listCC[$i][0].'.txt','r');
                if (!$fileOpen){
                    echo 'ERROR: No ha sido posible abrir el archivo'.$listCC[$i].'. Revisa su nombre y sus permisos.'; exit;
                }

                $index = 0; // contador de líneas
                while (!feof($fileOpen)) { // loop hasta que se llegue al final del archivo
                    $line = trim(fgets($fileOpen)); // guardamos toda la línea en $line como un string
                    $list[$index] = explode(";",$line);
                    $fileOpen++; // necesitamos llevar el puntero del archivo a la siguiente línea
                    $index++;
                }
                array_shift($list);
                $list2 = array();
                for ($j=0; $j < 5; $j++){
                    for ($k=0; $k < count($list); $k++){
                        if (strcmp($list[$k][0],strval($j+1)) == 0) {
                            $initialDate = explode('  ', $list[$k][3]);
                            $initialDate = $initialDate[0];
                            $endDate = explode('  ', $list[$k][4]);
                            $endDate = $endDate[0];  
                            $list2[$j][0] = "Week ".$list[$k][0]."\n (".trim($initialDate)." to \n".trim($endDate).")";
                            $list2[$j][1] = intval($list[$k][5]);
                        }
                    }
                }

                $list = $list2;
                
                $lastMonthASNs[$i] = $list;
            }

            $lastYearASNs = array();
            for ($i=0; $i < count($listCC); $i++) {
                if (file_exists('outputs_National_View/1_Number_ASNs_origin_in_more_than_1_IXP_per_country_lastyear/LastYear__number_visible_origin_ASNs_in_more_than_1_IXP_of_'.$listCC[$i][0].'.txt') == 0) {
                    $file = fopen('outputs_National_View/1_Number_ASNs_origin_in_more_than_1_IXP_per_country_lastyear/LastYear__number_visible_origin_ASNs_in_more_than_1_IXP_of_'.$listCC[$i][0].'.txt', "w");
                    fwrite($file, "" . PHP_EOL);
                    fclose($file);
                }
                $fileOpen = fopen('outputs_National_View/1_Number_ASNs_origin_in_more_than_1_IXP_per_country_lastyear/LastYear__number_visible_origin_ASNs_in_more_than_1_IXP_of_'.$listCC[$i][0].'.txt','r');
                if (!$fileOpen){
                    echo 'ERROR: No ha sido posible abrir el archivo'.$listCC[$i].'. Revisa su nombre y sus permisos.'; exit;
                }

                for ($z = 0; $z <= 12; $z++) {
                    $months[] = date("m-Y", strtotime( date( 'Y-m-01' )." -$z months"));
                }

                $prueba = array();
                for ($z=0; $z < count($months); $z++) {
                    $aux = explode("-",$months[$z]);
                    $aux[0] = (string)intval($aux[0]); 
                    $prueba[$z] = $aux[0].'-'.$aux[1].';0';
                }

                $prueba = array_reverse($prueba);
                $month = intval(date("m"));
                $plantilla = array();
                for ($k=0; $k < 13; $k++) { 
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
                        if (strcmp(trim($plantilla[$k][0]), trim($list[$j][0])) == 0) {
                            $plantilla[$k][1] = $list[$j][1];
                        }
                    }
                } 
                $lastYearASNs[$i] = $plantilla;
            }

            $multiYearASNs = array();
            for ($i=0; $i < count($listCC); $i++) {
                if (file_exists('outputs_National_View/1_Number_ASNs_origin_in_more_than_1_IXP_per_country_multiyear/MultiYear__number_visible_origin_ASNs_in_more_than_1_IXP_of_'.$listCC[$i][0].'.txt') == 0) {
                    $file = fopen('outputs_National_View/1_Number_ASNs_origin_in_more_than_1_IXP_per_country_multiyear/MultiYear__number_visible_origin_ASNs_in_more_than_1_IXP_of_'.$listCC[$i][0].'.txt', "w");
                    fwrite($file, "" . PHP_EOL);
                    fclose($file);
                }
                $fileOpen = fopen('outputs_National_View/1_Number_ASNs_origin_in_more_than_1_IXP_per_country_multiyear/MultiYear__number_visible_origin_ASNs_in_more_than_1_IXP_of_'.$listCC[$i][0].'.txt','r');
                if (!$fileOpen){
                    echo 'ERROR: No ha sido posible abrir el archivo'.$listCC[$i].'. Revisa su nombre y sus permisos.'; exit;
                }

                $list =  array();
                $index = 0; // contador de líneas
                while (!feof($fileOpen)) { // loop hasta que se llegue al final del archivo
                    $line = trim(fgets($fileOpen)); // guardamos toda la línea en $line como un string
                    $list[$index] = explode(";",$line);
                    $fileOpen++; // necesitamos llevar el puntero del archivo a la siguiente línea
                    $index++;
                }
            
                array_shift($list);
                $list2 = array();

                for ($j=0; $j < intval(date("Y"))-2004; $j++){
                    $anio = trim((string)(intval(date("Y"))-$j));
                    for ($k=0; $k < count($list); $k++){ 
                        if (strcmp($list[$k][0],$anio) == 0) {
                            $list2[$j][0] = $list[$k][0];
                            $list2[$j][1] = intval($list[$k][1]);
                        }
                    }
                }
                
                $years = array();
                for ($j = 0; $j <= intval(date("Y"))-2005; $j++) {
                        $years[$j][0] = (string)($j+2005);
                        $years[$j][1] = 0;
                }
                
                for ($j=0; $j <count($years); $j++) { 
                    for ($k=0; $k <count($list2) ; $k++) { 
                        if(strcmp($years[$j][0], $list2[$k][0]) == 0){
                            $years[$j][1] = $list2[$k][1];
                        }
                    }
                }

                $multiYearPrefixes[$i] = $years;
            }


        ?>
        <script type="text/javascript" src="//cdnjs.cloudflare.com/ajax/libs/jquery/2.0.3/jquery.min.js"></script>
        <script type="text/javascript" src="https://www.google.com/jsapi"></script>
        <script type="text/javascript">
            
            var lastMonthASNs = (<?php echo json_encode($lastMonthASNs)?>);
            var lastYearASNs = (<?php echo json_encode($lastYearASNs)?>);
            var multiYearASNs = (<?php echo json_encode($multiYearPrefixes)?>);
            var years = (<?php echo json_encode($years)?>);
            var listIXP = (<?php echo json_encode($listIXP)?>);
            var listCC = (<?php echo json_encode($listCC)?>);
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
                };
            };

            function paint() {

                var seleccionado = document.getElementById("selectIXP");
                var numero = seleccionado.selectedIndex;
                console.log(numero)

                if (numero == 0) {
                    drawChart(numero);
                }else{
                    drawChart(numero-1);
                    console.log('entrando')
                    var titulo = document.getElementById("titulo1");
                    var titulo2 = document.getElementById("titulo2");
                    var titulo3 = document.getElementById("titulo3");
                    IXP = (seleccionado.value);
                    console.log('asasas'+IXP)
                    titulo.innerHTML = "Aggregate Number of Unique Origin ASNs at all IXPs in "+IXP;
                    titulo2.innerHTML = "Aggregate Number of Unique Origin ASNs at all IXPs in "+IXP;
                    titulo3.innerHTML = "Aggregate Number of Unique Origin ASNs at all IXPs in "+IXP
                }
            }

            function chargeList(){
                if (charge== 0) {
                    var sel = document.getElementById('selectIXP');
                    for (var i = 0; i <listIXP.length; i++) {
                        var opt = document.createElement('option');
                        opt.innerHTML = listCC[i][1]+" ("+listCC[i][0]+")";
                        opt.value = listCC[i][0];
                        sel.appendChild(opt);
                    }
                }
                charge = 1;
            }

            function drawChart(i) {
                /*.........................*/
                var data = new google.visualization.DataTable();
                data.addColumn('string', 'Years');
                data.addColumn('number', '# Origin ASNs');

                data.addRows(lastMonthASNs[i]);

                var options = {
                    animation:{ duration: 1000,
                                easing: 'out',
                                startup: true},
                    width: 1000,
                    height: 300,
                    hAxis: {
                        title: 'Date thresholds', 
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

                var chart = new google.visualization.SteppedAreaChart(document.getElementById('originASNs'));
                chart.draw(data, options);

                /*.........................*/
                 var data = new google.visualization.DataTable();
                data.addColumn('string', 'Years');
                data.addColumn('number', '# Origin ASNs');

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
                 /*.........................*/
                var data = new google.visualization.DataTable();
                data.addColumn('string', 'Years');
                data.addColumn('number', '# Origin ASNs');

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
            }

            function descarga1(){
                console.log("adddd")
                var seleccionado = document.getElementById("selectIXP");
                var numero = seleccionado.selectedIndex;
                if (numero == 0) {
                    alert("Select an IXP");
                }else{
                    IXP = (seleccionado.value);
                    console.log (IXP)
                    downloadURI('outputs_National_View/1_Number_ASNs_origin_in_more_than_1_IXP_per_country_lastmonth/LastMonth__list_visible_ASNs_peering_at_IXP_'+IXP+'.txt','Last_5_week_number_of_Peering_ASNs_at_'+IXP+'.txt');                
                }
                
            }

            function descarga2(){
                console.log("adddd")
                var seleccionado = document.getElementById("selectIXP");
                var numero = seleccionado.selectedIndex;
                if (numero == 0) {
                    alert("Select an IXP");
                }else{
                    IXP = (seleccionado.value);
                    console.log (IXP)
                    downloadURI('outputs_National_View/1_Number_ASNs_origin_in_more_than_1_IXP_per_country_lastyear/LastYear__list_visible_ASNs_peering_at_IXP_'+IXP+'.txt','Last_12_Months_number_of_Peering_ASNs_at_'+IXP+'.txt');
                }
                
            }

            function descarga3(){
                console.log("adddd")
                var seleccionado = document.getElementById("selectIXP");
                var numero = seleccionado.selectedIndex;
                if (numero == 0) {
                    alert("Select an IXP");
                }else{
                    IXP = (seleccionado.value)
                    console.log (IXP)
                    downloadURI('outputs_National_View/1_Number_ASNs_origin_in_more_than_1_IXP_per_country_multiyear/MultiYear__list_visible_ASNs_origin_at_IXP_'+IXP+'.txt','Multiyear_number_of_Peering_ASNs_at_'+IXP+'.txt');
                }
                
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
                    <p class ="titulo" id="titulo1">Aggregate Number of Unique Origin ASNs at all IXPs in CC</p>     
                    <p id="subtitulo">Per week over the last month</p>
                </div>
                <div id="originASNs" style="width: 1000px; height: 300px;"></div>
                <div id= "botonDescarga">
                   <img onclick="javascript:descarga1();"id="enlaceDesgarga" src="images/dbutton.png" height="30">
                </div>
            </div>
            <div id="separador"></div>
            <div id="parrafos">
                <p class ="titulo" id="titulo2">Aggregate Number of Unique Origin ASNs at all IXPs in CC</p>     
                <p id="subtitulo">Per month over the last year</p>
            </div>
            <div id="lastYear" style="width: 1000px; height: 300px;"></div>
            <div id= "botonDescarga">
                   <img onclick="javascript:descarga2();" id="enlaceDesgarga" src="images/dbutton.png" height="30">
            </div>
            <div id="separador"></div>
            <div id="parrafos">
                <p class ="titulo" id="titulo3">Aggregate Number of Unique Origin ASNs at all IXPs in CC</p>     
                <p id="subtitulo">Per year over the historical Data (2005 up to now)</p>
            </div>
            <div id="multiYear" style="width: 1000px; height: 300px;"></div>
            <div id= "botonDescarga">
                   <img onclick="javascript:descarga3();" id="enlaceDesgarga" src="images/dbutton.png" height="30">
            </div>
        </div>
    </body>
</html>

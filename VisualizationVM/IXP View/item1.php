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

            //Origin
            $lastMonthPrefixes = array();
            for ($i=0; $i < count($listIXP); $i++) {
                if (file_exists('outputs/1_Number_prefixes_visibles_at_an_IXP_lastmonth/LastMonth__number_visible_prefixes_at_IXP_'.$listIXP[$i][0].'.txt') == 0) {
                    $file = fopen('outputs/1_Number_prefixes_visibles_at_an_IXP_lastmonth/LastMonth__number_visible_prefixes_at_IXP_'.$listIXP[$i][0].'.txt', "w");
                    fwrite($file, "" . PHP_EOL);
                    fclose($file);
                } 
                $fileOpen = fopen('outputs/1_Number_prefixes_visibles_at_an_IXP_lastmonth/LastMonth__number_visible_prefixes_at_IXP_'.$listIXP[$i][0].'.txt','r');
                if (!$fileOpen){
                    echo 'ERROR: No ha sido posible abrir el archivo1'.$listIXP[$i][0].'. Revisa su nombre y sus permisos.'; exit;
                }

                $index = 0; // contador de líneas
                while (!feof($fileOpen)) { // loop hasta que se llegue al final del archivo
                    $line = trim(fgets($fileOpen)); // guardamos toda la línea en $line como un string
                    $pos = strpos($line, '#');
                    if($pos === false){
                        $list[$index] = explode(";",$line);
                        $fileOpen++; // necesitamos llevar el puntero del archivo a la siguiente línea
                        $index++;
                    }
                    
                }
                $list2 = array();
                for ($j=0; $j < 5; $j++) {
                    $initialDate = explode('  ', $list[$j][3]);
                    $initialDate = $initialDate[0];
                    $endDate = explode('  ', $list[$j][4]);
                    $endDate = $endDate[0];  
                    $list2[$j][0] = "Week ".$list[$j][0]."\n (".trim($initialDate)." to \n".trim($endDate).")";
                    $list2[$j][1] = intval($list[$j][5]);
                    $list2[$j][2] = intval($list[$j][6]);
                }
                $list = $list2;
                $lastMonthPrefixes[$i] = $list;
            }

         $lastYearPrefixes = array();
            for ($i=0; $i < count($listIXP); $i++) {
                 if (file_exists('outputs/1_Number_prefixes_visibles_at_an_IXP_multiyear_lastyear/LastYear__number_visible_prefixes_at_IXP_'.$listIXP[$i][0].'.txt') == 0) {
                    $file = fopen('outputs/1_Number_prefixes_visibles_at_an_IXP_multiyear_lastyear/LastYear__number_visible_prefixes_at_IXP_'.$listIXP[$i][0].'.txt', "w");
                    fwrite($file, "" . PHP_EOL);
                    fclose($file);
                } 
                $fileOpen = fopen('outputs/1_Number_prefixes_visibles_at_an_IXP_multiyear_lastyear/LastYear__number_visible_prefixes_at_IXP_'.$listIXP[$i][0].'.txt','r');
                if (!$fileOpen){
                    echo 'ERROR: No ha sido posible abrir el archivo2'.$listIXP[$i][0].'. Revisa su nombre y sus permisos.'; exit;
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
                            $plantilla[$k][2] = $list[$j][2];
                        }
                    }
                } 
                $lastYearPrefixes[$i] = $plantilla;
            }

            $multiYearPrefixes = array();
            for ($i=0; $i < count($listIXP); $i++) { 
                 if (file_exists('outputs/1_Number_prefixes_visibles_at_an_IXP_multiyear_lastyear/MultiYear__number_visible_prefixes_at_IXP_'.$listIXP[$i][0].'.txt') == 0) {
                    $file = fopen('outputs/1_Number_prefixes_visibles_at_an_IXP_multiyear_lastyear/MultiYear__number_visible_prefixes_at_IXP_'.$listIXP[$i][0].'.txt', "w");
                    fwrite($file, "" . PHP_EOL);
                    fclose($file);
                } 
                $fileOpen = fopen('outputs/1_Number_prefixes_visibles_at_an_IXP_multiyear_lastyear/MultiYear__number_visible_prefixes_at_IXP_'.$listIXP[$i][0].'.txt','r');
                if (!$fileOpen){
                    echo 'ERROR: No ha sido posible abrir el archivo3'.$listIXP[$i][0].'. Revisa su nombre y sus permisos.'; exit;
                }

                $index = 0; // contador de líneas
                $list = array();
                while (!feof($fileOpen)) { // loop hasta que se llegue al final del archivo
                    $line = trim(fgets($fileOpen)); // guardamos toda la línea en $line como un string
                    $pos = strpos($line, '#');
                    if($pos === false){
                        $list[$index] = explode(";",$line);
                        $fileOpen++; // necesitamos llevar el puntero del archivo a la siguiente línea
                        $index++;
                    }
                }
                $list2 = array();
                for ($j=0; $j < intval(date("Y"))-2004; $j++) {
                    $list2[$j][0] = $list[$j][0];
                    $list2[$j][1] = intval($list[$j][1]);
                    $list2[$j][2] = intval($list[$j][2]);
                }
                $list = $list2;
                $multiYearPrefixes[$i] = $list;
            }

    
        ?>
        <script type="text/javascript" src="//cdnjs.cloudflare.com/ajax/libs/jquery/2.0.3/jquery.min.js"></script>
        <script type="text/javascript" src="https://www.google.com/jsapi"></script>
        <script type="text/javascript">
    
            var listIXP = (<?php echo json_encode($listIXP)?>);
            var lastMonthPrefixes = (<?php echo json_encode($lastMonthPrefixes)?>);
            var lastYearPrefixes = (<?php echo json_encode($lastYearPrefixes)?>);
            var multiYearPrefixes = (<?php echo json_encode($multiYearPrefixes)?>);
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
             for (var i = 0; i < lastYearPrefixes.length; i++) {
                    for (var j = 0; j < lastYearPrefixes[i].length; j++) {
                        aux = lastYearPrefixes[i][j][0].split("-");
                        aux[0] = month[parseInt(aux[0])-1];
                        lastYearPrefixes[i][j][0] = aux[0]+" "+aux[1]
                        lastYearPrefixes[i][j][1] = parseInt(lastYearPrefixes[i][j][1]);
                        lastYearPrefixes[i][j][2] = parseInt(lastYearPrefixes[i][j][2]);
                    };
                };

            function paint() {


                var seleccionado = document.getElementById("selectIXP");
                var numero = seleccionado.selectedIndex;

                if (numero == 0) {
                    drawChart(numero);
                    var titulo = document.getElementById("titulo1");
                    var titulo3 = document.getElementById("titulo2");
                    var titulo2 = document.getElementById("titulo3");
                    titulo.innerHTML = "Number of visible Prefixes at "+listIXP[0][0];
                    titulo2.innerHTML = "Number of visible Prefixes at "+listIXP[0][0];
                    titulo3.innerHTML = "Number of visible Prefixes at "+listIXP[0][0];
                }else{
                    drawChart(numero-1);
                    var titulo = document.getElementById("titulo1");
                    var titulo3 = document.getElementById("titulo2");
                    var titulo2 = document.getElementById("titulo3");
                    IXP = (seleccionado.value).split(",")[0];
                    titulo.innerHTML = "Number of visible Prefixes at "+IXP;
                    titulo2.innerHTML = "Number of visible Prefixes at "+IXP;
                    titulo3.innerHTML = "Number of visible Prefixes at "+IXP;
                }
            }

            function drawChart(i) {
                /*.........................*/
                var data = new google.visualization.DataTable();
                data.addColumn('string', 'Years');
                data.addColumn('number', '# Prefixes');
                data.addColumn('number', '# Bogon Prefixes');

                data.addRows(lastMonthPrefixes[i]);

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
                        title: 'Number of Prefixes',
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
                data.addColumn('number', '# Prefixes');
                data.addColumn('number', '# Bogon Prefixes');

                data.addRows(lastYearPrefixes[i]);

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
                        title: 'Number of Prefixes',
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
                data.addColumn('number', '# Prefixes');
                data.addColumn('number', '# Bogon Prefixes');

                data.addRows(multiYearPrefixes[i]);

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
                        title: 'Number of Prefixes',
                        textStyle:{fontName: 'Trebuchet MS'},
                        titleTextStyle:{fontName: 'Trebuchet MS'}},
                    legend: {textStyle:{fontName: 'Trebuchet MS'}},
                    tooltip: {textStyle:{fontName: 'Trebuchet MS'}},
                    colors: ['#53A8FB', '#F1CA3A'],
                };

                var chart = new google.visualization.SteppedAreaChart(document.getElementById('multiYear'));
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
                    downloadURI('outputs/1_Number_prefixes_visibles_at_an_IXP_lastmonth/LastMonth__list_visible_prefixes_at_IXP_'+IXP+'.txt','Last_5_week_number_of_viseble_prefixes_at_'+IXP+'_raw_data.txt');
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
                    downloadURI('outputs/1_Number_prefixes_visibles_at_an_IXP_multiyear_lastyear/LastYear__list_visible_prefixes_at_IXP_'+IXP+'.txt','Last_12_months_number_of_viseble_prefixes_at_'+IXP+'_raw_data.txt');
                }
                
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
                    downloadURI('outputs/1_Number_prefixes_visibles_at_an_IXP_multiyear_lastyear/MultiYear__list_visible_prefixes_at_IXP_'+IXP+'.txt','Multiyear_number_of_viseble_prefixes_at_'+IXP+'_raw_data.txt');
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
                    <option><b>Select IXP :</b></option>
                </select>
            </div>
            <div>
                <div id="parrafos">
                    <p class ="titulo" id="titulo1">Number of visible Prefixes at the IXP</p>     
                    <p id="subtitulo">Per week over the last month</p>
                </div>
                <div id="originASNs" style="width: 1000px; height: 300px;"></div>
                <div id= "botonDescarga">
                   <img onclick="javascript:descarga1();"id="enlaceDesgarga" src="images/dbutton.png" height="30">
                </div>
            </div>

            <div id="separador"></div>
            <div id="parrafos">
                <p class ="titulo" id="titulo2">Number of visible Prefixes at the IXP</p>     
                <p id="subtitulo">Per month over the last year</p>
            </div>
            <div id="lastYear" style="width: 1000px; height: 300px;"></div>
            <div id= "botonDescarga">
                   <img onclick="javascript:descarga2();" id="enlaceDesgarga" src="images/dbutton.png" height="30">
            </div>

            <div id="separador"></div>
            <div id="parrafos">
                <p class ="titulo" id="titulo3">Number of visible Prefixes at the IXP</p>     
                <p id="subtitulo">Per year over the historical Data (2005 up to now)</p>
            </div>
            <div id="multiYear" style="width: 1000px; height: 300px;"></div>
            <div id= "botonDescarga">
                   <img onclick="javascript:descarga3();" id="enlaceDesgarga" src="images/dbutton.png" height="30">
            </div>
        </div>
    </body>
</html>

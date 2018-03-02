<html>
    <head>
        <link rel="stylesheet" href="css/select.css">
        <?php
            ini_set('memory_limit', '-1');

            $lastMonthASNs = array();
            
            if (file_exists('outputs_Regional_View/1_Number_ASNs_peering_in_more_than_1_IXP_in_Region_lastmonth/LastMonth__Total_Number_unique_peering_ASNs_seen_at_1_IXP_and_more.txt') == 0) {
                $file = fopen('outputs_Regional_View/1_Number_ASNs_peering_in_more_than_1_IXP_in_Region_lastmonth/LastMonth__Total_Number_unique_peering_ASNs_seen_at_1_IXP_and_more.txt', "w");
                fwrite($file, "" . PHP_EOL);
                fclose($file);
            }
            $fileOpen = fopen('outputs_Regional_View/1_Number_ASNs_peering_in_more_than_1_IXP_in_Region_lastmonth/LastMonth__Total_Number_unique_peering_ASNs_seen_at_1_IXP_and_more.txt','r');
            if (!$fileOpen){
                echo 'ERROR: No ha sido posible abrir el archivo. Revisa su nombre y sus permisos.'; exit;
            }

            $index = 0; // contador de líneas
            while (!feof($fileOpen)) { // loop hasta que se llegue al final del archivo
                $line = trim(fgets($fileOpen)); // guardamos toda la línea en $line como un string
                if (strpos($line, '%') !== false){
                    $list[$index] = explode(";",$line);
                    $index++;
                }
                $fileOpen++; // necesitamos llevar el puntero del archivo a la siguiente línea
            }
            
            $list2 = array();
            for ($j=0; $j < count($list); $j++) {
                $list2[$j][0] = $list[$j][0];
                $list2[$j][1] = intval($list[$j][1]);
            }
            $lastMonthASNs = $list2;

            /*-----------------------------------------------------------------------*/

            $lastYearASNs = array();
            
            if (file_exists('outputs_Regional_View/1_Number_ASNs_peering_in_more_than_1_IXP_in_Region_lastyear/LastYear__Total_Number_unique_Peering_ASNs_seen_at_1_IXP_and_more.txt') == 0) {
                $file = fopen('outputs_Regional_View/1_Number_ASNs_peering_in_more_than_1_IXP_in_Region_lastyear/LastYear__Total_Number_unique_Peering_ASNs_seen_at_1_IXP_and_more.txt', "w");
                fwrite($file, "" . PHP_EOL);
                fclose($file);
            }
            $fileOpen = fopen('outputs_Regional_View/1_Number_ASNs_peering_in_more_than_1_IXP_in_Region_lastyear/LastYear__Total_Number_unique_Peering_ASNs_seen_at_1_IXP_and_more.txt','r');
            if (!$fileOpen){
                echo 'ERROR: No ha sido posible abrir el archivo. Revisa su nombre y sus permisos.'; exit;
            }

            $index = 0; // contador de líneas
            while (!feof($fileOpen)) { // loop hasta que se llegue al final del archivo
                $line = trim(fgets($fileOpen)); // guardamos toda la línea en $line como un string
                if (strpos($line, '%') !== false){
                    $list[$index] = explode(";",$line);
                    $index++;
                }
                $fileOpen++; // necesitamos llevar el puntero del archivo a la siguiente línea
            }
            $list2 = array();
            for ($j=0; $j < count($list); $j++) {
                $list2[$j][0] = $list[$j][0];
                $list2[$j][1] = intval($list[$j][1]);
            }
            $lastYearASNs = $list2;

            /*-----------------------------------------------------------------------*/

            $lessYearASNs = array();
            if (file_exists('outputs_Regional_View/1_Number_ASNs_peering_in_more_than_1_IXP_in_Region_multiyear/MultiYear__Total_Number_unique_Peering_ASNs_seen_at_1_IXP_and_more__'.date("Y").'.txt') == 0) {
                $file = fopen('outputs_Regional_View/1_Number_ASNs_peering_in_more_than_1_IXP_in_Region_multiyear/MultiYear__Total_Number_unique_Peering_ASNs_seen_at_1_IXP_and_more__'.date("Y").'.txt', "w");
                fwrite($file, "" . PHP_EOL);
                fclose($file);
            }
            $fileOpen = fopen('outputs_Regional_View/1_Number_ASNs_peering_in_more_than_1_IXP_in_Region_multiyear/MultiYear__Total_Number_unique_Peering_ASNs_seen_at_1_IXP_and_more__'.date("Y").'.txt','r');
            if (!$fileOpen){
                echo 'ERROR: No ha sido posible abrir el archivo. Revisa su nombre y sus permisos.'; exit;
            }

            $index = 0; // contador de líneas
            while (!feof($fileOpen)) { // loop hasta que se llegue al final del archivo
                $line = trim(fgets($fileOpen)); // guardamos toda la línea en $line como un string
                if (strpos($line, '%') !== false){
                    $list[$index] = explode(";",$line);
                    $index++;
                }
                $fileOpen++; // necesitamos llevar el puntero del archivo a la siguiente línea
            }
            
            $list2 = array();
            for ($j=0; $j < count($list); $j++) {
                $list2[$j][0] = $list[$j][0];
                $list2[$j][1] = intval($list[$j][1]);
            }
            $lessYearASNs = $list2;

            /*-----------------------------------------------------------------------*/

            $less2YearASNs = array();
            
            if (file_exists('outputs_Regional_View/1_Number_ASNs_peering_in_more_than_1_IXP_in_Region_multiyear/MultiYear__Total_Number_unique_Peering_ASNs_seen_at_1_IXP_and_more__'.strval(intval(date("Y"))-1).'.txt') == 0) {
                $file = fopen('outputs_Regional_View/1_Number_ASNs_peering_in_more_than_1_IXP_in_Region_multiyear/MultiYear__Total_Number_unique_Peering_ASNs_seen_at_1_IXP_and_more__'.strval(intval(date("Y"))-1).'.txt', "w");
                fwrite($file, "" . PHP_EOL);
                fclose($file);
            }
            $fileOpen = fopen('outputs_Regional_View/1_Number_ASNs_peering_in_more_than_1_IXP_in_Region_multiyear/MultiYear__Total_Number_unique_Peering_ASNs_seen_at_1_IXP_and_more__'.strval(intval(date("Y"))-1).'.txt','r');
            if (!$fileOpen){
                echo 'ERROR: No ha sido posible abrir el archivo. Revisa su nombre y sus permisos.'; exit;
            }

            $index = 0; // contador de líneas
            while (!feof($fileOpen)) { // loop hasta que se llegue al final del archivo
                $line = trim(fgets($fileOpen)); // guardamos toda la línea en $line como un string
                if (strpos($line, '%') !== false){
                    $list[$index] = explode(";",$line);
                    $index++;
                }
                $fileOpen++; // necesitamos llevar el puntero del archivo a la siguiente línea
            }
            
            $list2 = array();
            for ($j=0; $j < count($list); $j++) {
                $list2[$j][0] = $list[$j][0];
                $list2[$j][1] = intval($list[$j][1]);
            }
            $less2YearASNs = $list2;

            /*-----------------------------------------------------------------------*/
            
            $listYears = array();

            $index = 0; // contador de líneas
            for ($i=0; $i <intval(date("Y"))-2007 ; $i++) { 
                array_push($listYears,strval(intval(date("Y"))-$i-2));
            }

            /*----------------------------------------------------------------------*/

            $list1select = array();

            for ($i=0; $i < count($listYears); $i++) {
                if (file_exists('outputs_Regional_View/1_Number_ASNs_peering_in_more_than_1_IXP_in_Region_multiyear/MultiYear__Total_Number_unique_Peering_ASNs_seen_at_1_IXP_and_more__'.$listYears[$i].'.txt') == 0) {
                    $file = fopen('outputs_Regional_View/1_Number_ASNs_peering_in_more_than_1_IXP_in_Region_multiyear/MultiYear__Total_Number_unique_Peering_ASNs_seen_at_1_IXP_and_more__'.$listYears[$i].'.txt', "w");
                    fwrite($file, "" . PHP_EOL);
                    fclose($file);
                }
                $fileOpen = fopen('outputs_Regional_View/1_Number_ASNs_peering_in_more_than_1_IXP_in_Region_multiyear/MultiYear__Total_Number_unique_Peering_ASNs_seen_at_1_IXP_and_more__'.$listYears[$i].'.txt','r');
                if (!$fileOpen){
                    echo 'ERROR: No ha sido posible abrir el archivo. Revisa su nombre y sus permisos.'; exit;
                }

                $index = 0; // contador de líneas
                while (!feof($fileOpen)) { // loop hasta que se llegue al final del archivo
                    $line = trim(fgets($fileOpen)); // guardamos toda la línea en $line como un string
                    if (strpos($line, '%') !== false){
                        $list[$index] = explode(";",$line);
                        $index++;
                    }
                    $fileOpen++; // necesitamos llevar el puntero del archivo a la siguiente línea
                }
            
                $list2 = array();
                for ($j=0; $j < count($list); $j++) {
                    $list2[$j][0] = $list[$j][0];
                    $list2[$j][1] = intval($list[$j][1]);
                }

                $list1select[$i] = $list2;
            }
    
        ?>
        <script type="text/javascript" src="//cdnjs.cloudflare.com/ajax/libs/jquery/2.0.3/jquery.min.js"></script>
        <script type="text/javascript" src="https://www.google.com/jsapi"></script>
        <script type="text/javascript">

            var listYears = (<?php echo json_encode($listYears)?>);
            var lastMonthASNs = (<?php echo json_encode($lastMonthASNs)?>);
            var lastYearASNs = (<?php echo json_encode($lastYearASNs)?>);
            var lessYearASNs = (<?php echo json_encode($lessYearASNs)?>);
            var less2YearASNs = (<?php echo json_encode($less2YearASNs)?>);
            var listYears = (<?php echo json_encode($listYears)?>);
            var list1select = (<?php echo json_encode($list1select)?>);
            var charge = 0;
            var d = new Date();
            var n = d.getFullYear();
            
            /*
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
            month[11] = "Dec";*/

            google.load("visualization", "1", {packages:["corechart"]});
            google.setOnLoadCallback(paint);

            /*
            for (var i = 0; i < lastYearASNs.length; i++) {
                for (var j = 0; j < lastYearASNs[i].length; j++) {
                    aux = lastYearASNs[i][j][0].split("-");
                    aux[0] = month[parseInt(aux[0])-1];
                    lastYearASNs[i][j][0] = aux[0]+" "+aux[1]
                    lastYearASNs[i][j][1] = parseInt(lastYearASNs[i][j][1]);
                };
            };*/

            function paint(){
                var seleccionado = document.getElementById("selectYear");
                var numero = seleccionado.selectedIndex;
                if (numero == 0) {
                    numero = 1;
                };
                var valor = seleccionado.value;
                document.getElementById("subtitulo3").innerHTML = "In "+ listYears[numero-1];
                document.getElementById("subtitulo1").innerHTML = "In "+ (n-1);
                document.getElementById("subtitulo2").innerHTML = "In "+ (n);
            
                drawChart(numero-1);
            }

            function drawChart(i) {
                var data = new google.visualization.DataTable();

                data.addColumn('string', 'Country');
                data.addColumn('number', 'Percentage');

                data.addRows(lastMonthASNs);

                var options = {
                  'title':'Peering ASNs',
                  is3D: false,
                  fontName: 'Trebuchet MS',
                  sliceVisibilityThreshold: 0

                };

                var chart = new google.visualization.PieChart(document.getElementById('piechart11'));
                google.visualization.events.addListener(chart, 'select', selectHandler);
                chart.draw(data, options);

                function selectHandler() {
                var selectedItem = chart.getSelection()[0]
                    console.log(selectedItem.row)
                    if (selectedItem.row == 0){
                        var value = data.getValue(selectedItem.row,0);
                        if (confirm("Do you want to download this file?") == true) {
                            downloadURI("outputs_Regional_View/1_Number_ASNs_peering_in_more_than_1_IXP_in_Region_lastmonth/LastMonth__List_Peering_ASNs_0percent_20percent.txt","0-20_lastmonth.txt"); 
                        }
                    };
                    if (selectedItem.row == 1){
                        var value = data.getValue(selectedItem.row,0);
                        if (confirm("Do you want to download this file?") == true) {
                            downloadURI("outputs_Regional_View/1_Number_ASNs_peering_in_more_than_1_IXP_in_Region_lastmonth/LastMonth__List_Peering_ASNs_20percent_40percent.txt","20-40_lastmonth.txt"); 
                        }
                    };
                    if (selectedItem.row == 2) {
                        var value = data.getValue(selectedItem.row,0);
                        if (confirm("Do you want to download this file?") == true) {
                            downloadURI("outputs_Regional_View/1_Number_ASNs_peering_in_more_than_1_IXP_in_Region_lastmonth/LastMonth__List_Peering_ASNs_40percent_60percent.txt","40-60_lastmonth.txt");
                        }
                    };
                    if (selectedItem.row == 3) {
                        var value = data.getValue(selectedItem.row,0);
                        if (confirm("Do you want to download this file?") == true) {
                            downloadURI("outputs_Regional_View/1_Number_ASNs_peering_in_more_than_1_IXP_in_Region_lastmonth/LastMonth__List_Peering_ASNs_60percent_80percent.txt","60-80_lastmonth.txt");
                        }
                    };
                    if (selectedItem.row == 4) {
                        var value = data.getValue(selectedItem.row,0);
                        if (confirm("Do you want to download this file?") == true) {
                            downloadURI("outputs_Regional_View/1_Number_ASNs_peering_in_more_than_1_IXP_in_Region_lastmonth/LastMonth__List_Peering_ASNs_80percent_1000percent.txt","80-100_lastmonth.txt");
                        }
                    };
                };

                /*----------------------------------------------------------------------------*/

                var data2 = new google.visualization.DataTable();

                data2.addColumn('string', 'Country');
                data2.addColumn('number', 'Percentage');

                data2.addRows(lastYearASNs);

                var options2 = {
                  'title':'Peering ASNs',
                  is3D: false,
                  fontName: 'Trebuchet MS',
                  sliceVisibilityThreshold: 0
                };

                var chart2 = new google.visualization.PieChart(document.getElementById('piechart12'));
                google.visualization.events.addListener(chart2, 'select', selectHandler2);
                chart2.draw(data2, options2);

                function selectHandler2() {
                    var selectedItem2 = chart2.getSelection()[0]
                    console.log(selectedItem2.row)
                    if (selectedItem2.row == 0){
                        var value = data.getValue(selectedItem2.row,0);
                        if (confirm("Do you want to download this file?") == true) {
                            downloadURI("outputs_Regional_View/1_Number_ASNs_peering_in_more_than_1_IXP_in_Region_lastyear/LastYear__List_Peering_ASNs_0percent_20percent.txt","0-20_lastyear.txt"); 
                        }
                    };
                    if (selectedItem2.row == 1){
                        var value = data.getValue(selectedItem2.row,0);
                        if (confirm("Do you want to download this file?") == true) {
                            downloadURI("outputs_Regional_View/1_Number_ASNs_peering_in_more_than_1_IXP_in_Region_lastyear/LastYear__List_Peering_ASNs_20percent_40percent.txt","20-40_lastyear.txt"); 
                        }
                    };
                    if (selectedItem2.row == 2) {
                        var value = data.getValue(selectedItem2.row,0);
                        if (confirm("Do you want to download this file?") == true) {
                            downloadURI("outputs_Regional_View/1_Number_ASNs_peering_in_more_than_1_IXP_in_Region_lastyear/LastYear__List_Peering_ASNs_40percent_60percent.txt","40-60_lastyear.txt");
                        }
                    };
                    if (selectedItem2.row == 3) {
                        var value = data.getValue(selectedItem2.row,0);
                        if (confirm("Do you want to download this file?") == true) {
                            downloadURI("outputs_Regional_View/1_Number_ASNs_peering_in_more_than_1_IXP_in_Region_lastyear/LastYear__List_Peering_ASNs_60percent_80percent.txt","60-80_lastyear.txt");
                        }
                    };
                    if (selectedItem2.row == 4) {
                        var value = data.getValue(selectedItem2.row,0);
                        if (confirm("Do you want to download this file?") == true) {
                            downloadURI("outputs_Regional_View/1_Number_ASNs_peering_in_more_than_1_IXP_in_Region_lastyear/LastYear__List_Peering_ASNs_80percent_100percent.txt","80-100_lastyear.txt");
                        }
                    };
                };

                /*----------------------------------------------------------------------------*/

                var data3 = new google.visualization.DataTable();

                data3.addColumn('string', 'Country');
                data3.addColumn('number', 'Percentage');

                data3.addRows(lessYearASNs);

                var options3 = {
                  'title':'Peering ASNs',
                  is3D: false,
                  fontName: 'Trebuchet MS',
                  sliceVisibilityThreshold: 0

                };

                var chart3 = new google.visualization.PieChart(document.getElementById('piechart21'));
                google.visualization.events.addListener(chart3, 'select', selectHandler3);
                chart3.draw(data3, options3);

                function selectHandler3() {
                    var selectedItem3 = chart3.getSelection()[0]
                    console.log(selectedItem3.row)
                    if (selectedItem3.row == 0){
                        var value = data.getValue(selectedItem3.row,0);
                        if (confirm("Do you want to download this file?") == true) {
                            downloadURI("outputs_Regional_View/1_Number_ASNs_peering_in_more_than_1_IXP_in_Region_multiyear/MultiYear__List_Peering_ASNs_0percent_20percent_Year_"+(n)+".txt","0-20_lastyear.txt"); 
                        }
                    };
                    if (selectedItem3.row == 1){
                        var value = data.getValue(selectedItem3.row,0);
                        if (confirm("Do you want to download this file?") == true) {
                            downloadURI("outputs_Regional_View/1_Number_ASNs_peering_in_more_than_1_IXP_in_Region_multiyear/MultiYear__List_Peering_ASNs_20percent_40percent_Year_"+(n)+".txt","20-40_lastyear.txt"); 
                        }
                    };
                    if (selectedItem3.row == 2) {
                        var value = data.getValue(selectedItem3.row,0);
                        if (confirm("Do you want to download this file?") == true) {
                            downloadURI("outputs_Regional_View/1_Number_ASNs_peering_in_more_than_1_IXP_in_Region_multiyear/MultiYear__List_Peering_ASNs_40percent_60percent_"+(n)+".txt","40-60_lastyear.txt");
                        }
                    };
                    if (selectedItem3.row == 3) {
                        var value = data.getValue(selectedItem3.row,0);
                        if (confirm("Do you want to download this file?") == true) {
                            downloadURI("outputs_Regional_View/1_Number_ASNs_peering_in_more_than_1_IXP_in_Region_multiyear/MultiYear__List_Peering_ASNs_60percent_80percent_"+(n)+".txt","60-80_lastyear.txt");
                        }
                    };
                    if (selectedItem3.row == 4) {
                        var value = data.getValue(selectedItem3.row,0);
                        if (confirm("Do you want to download this file?") == true) {
                            downloadURI("outputs_Regional_View/1_Number_ASNs_peering_in_more_than_1_IXP_in_Region_multiyear/MultiYear__List_Peering_ASNs_80percent_100percent_"+(n)+".txt","80-100_lastyear.txt");
                        }
                    };
                };

                /*----------------------------------------------------------------------------*/

                var data4 = new google.visualization.DataTable();

                data4.addColumn('string', 'Country');
                data4.addColumn('number', 'Percentage');

                data4.addRows(less2YearASNs);

                var options4 = {
                  'title':'Peering ASNs',
                  is3D: false,
                  fontName: 'Trebuchet MS',
                  sliceVisibilityThreshold: 0
                };

                var chart4 = new google.visualization.PieChart(document.getElementById('piechart22'));
                google.visualization.events.addListener(chart4, 'select', selectHandler4);
                chart4.draw(data4, options4);

                function selectHandler4() {
                    var selectedItem4 = chart4.getSelection()[0]
                    console.log(selectedItem4.row)
                    if (selectedItem4.row == 0){
                        var value = data.getValue(selectedItem4.row,0);
                        if (confirm("Do you want to download this file?") == true) {
                            downloadURI("outputs_Regional_View/1_Number_ASNs_peering_in_more_than_1_IXP_in_Region_multiyear/MultiYear__List_Peering_ASNs_0percent_20percent_Year_"+(n-1)+".txt","0-20_lastyear.txt"); 
                        }
                    };
                    if (selectedItem4.row == 1){
                        var value = data.getValue(selectedItem4.row,0);
                        if (confirm("Do you want to download this file?") == true) {
                            downloadURI("outputs_Regional_View/1_Number_ASNs_peering_in_more_than_1_IXP_in_Region_multiyear/MultiYear__List_Peering_ASNs_20percent_40percent_Year_"+(n-1)+".txt","20-40_lastyear.txt"); 
                        }
                    };
                    if (selectedItem4.row == 2) {
                        var value = data.getValue(selectedItem4.row,0);
                        if (confirm("Do you want to download this file?") == true) {
                            downloadURI("outputs_Regional_View/1_Number_ASNs_peering_in_more_than_1_IXP_in_Region_multiyear/MultiYear__List_Peering_ASNs_40percent_60percent_"+(n-1)+".txt","40-60_lastyear.txt");
                        }
                    };
                    if (selectedItem4.row == 3) {
                        var value = data.getValue(selectedItem4.row,0);
                        if (confirm("Do you want to download this file?") == true) {
                            downloadURI("outputs_Regional_View/1_Number_ASNs_peering_in_more_than_1_IXP_in_Region_multiyear/MultiYear__List_Peering_ASNs_60percent_80percent_"+(n-1)+".txt","60-80_lastyear.txt");
                        }
                    };
                    if (selectedItem4.row == 4) {
                        var value = data.getValue(selectedItem4.row,0);
                        if (confirm("Do you want to download this file?") == true) {
                            downloadURI("outputs_Regional_View/1_Number_ASNs_peering_in_more_than_1_IXP_in_Region_multiyear/MultiYear__List_Peering_ASNs_80percent_100percent_"+(n-1)+".txt","80-100_lastyear.txt");
                        }
                    };
                };

                /*----------------------------------------------------------------------------*/

                var data5 = new google.visualization.DataTable();

                data5.addColumn('string', 'Country');
                data5.addColumn('number', 'Percentage');

                data5.addRows(list1select[i]);

                var options5 = {
                  'title':'Peering ASNs',
                  is3D: false,
                  fontName: 'Trebuchet MS',
                  sliceVisibilityThreshold: 0
                };

                var chart5 = new google.visualization.PieChart(document.getElementById('piechart3'));
                google.visualization.events.addListener(chart5, 'select', selectHandler5);
                chart5.draw(data5, options5);

                function selectHandler5() {
                    var selectedItem5 = chart5.getSelection()[0]
                    console.log(selectedItem5.row)
                    if (selectedItem5.row == 0){
                        var value = data.getValue(selectedItem5.row,0);
                        if (confirm("Do you want to download this file?") == true) {
                            downloadURI("outputs_Regional_View/1_Number_ASNs_peering_in_more_than_1_IXP_in_Region_multiyear/MultiYear__List_Peering_ASNs_0percent_20percent_Year_"+listYears[i]+".txt","0-20_lastyear.txt"); 
                        }
                    };
                    if (selectedItem5.row == 1){
                        var value = data.getValue(selectedItem5.row,0);
                        if (confirm("Do you want to download this file?") == true) {
                            downloadURI("outputs_Regional_View/1_Number_ASNs_peering_in_more_than_1_IXP_in_Region_multiyear/MultiYear__List_Peering_ASNs_20percent_40percent_Year_"+listYears[i]+".txt","20-40_lastyear.txt"); 
                        }
                    };
                    if (selectedItem5.row == 2) {
                        var value = data.getValue(selectedItem5.row,0);
                        if (confirm("Do you want to download this file?") == true) {
                            downloadURI("outputs_Regional_View/1_Number_ASNs_peering_in_more_than_1_IXP_in_Region_multiyear/MultiYear__List_Peering_ASNs_40percent_60percent_"+listYears[i]+".txt","40-60_lastyear.txt");
                        }
                    };
                    if (selectedItem5.row == 3) {
                        var value = data.getValue(selectedItem5.row,0);
                        if (confirm("Do you want to download this file?") == true) {
                            downloadURI("outputs_Regional_View/1_Number_ASNs_peering_in_more_than_1_IXP_in_Region_multiyear/MultiYear__List_Peering_ASNs_60percent_80percent_"+listYears[i]+".txt","60-80_lastyear.txt");
                        }
                    };
                    if (selectedItem5.row == 4) {
                        var value = data.getValue(selectedItem5.row,0);
                        if (confirm("Do you want to download this file?") == true) {
                            downloadURI("outputs_Regional_View/1_Number_ASNs_peering_in_more_than_1_IXP_in_Region_multiyear/MultiYear__List_Peering_ASNs_80percent_100percent_"+listYears[i]+".txt","80-100_lastyear.txt");
                        }
                    };
                };


            }

            function chargeList(){
                if (charge== 0) {
                    var sel = document.getElementById('selectYear');
                    for (var i = 0; i <listYears.length; i++) {
                        var opt = document.createElement('option');
                        opt.innerHTML = listYears[i];
                        opt.value = listYears[i];
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
                margin-left: 500px
            }
            #visibleASNs{
                margin-left: 100px;
            }
            #prefixes{
                margin-left: 100px;
            }
            #parrafos{
                margin-left: 10px;
            }
            #separador {
                margin-top: 15px;
            }
            #separador2 {
                margin-top: 25px;
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
            #subtitulo1{
                font-size: 14px;
                font-family: 'Trebuchet MS';
                color: #BDBDBD;
            }
            #subtitulo2{
                font-size: 14px;
                font-family: 'Trebuchet MS';
                color: #BDBDBD;
            }
            #subtitulo3{
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
        <div style="width: 1300px; height: 375px; margin-left:0px;">
                <div id="primero" style="width: 550px; height: 400px; margin-left:30px; display: inline-block;">
                    <div id="parrafos">
                        <p class ="titulo" id="titulo1">Number of Peering ASNs visible in one or more IXPs</p>     
                        <p id="subtitulo">Over the last month</p>
                    </div>
                    <div id="piechart11" style="width: 550px; height: 350px; float: left;"></div>
                </div>
                <div id="segundo" style="width: 550px; height: 400px; margin-left:30px; display: inline-block;">
                    <div id="parrafos">
                        <p class="titulo" id="titulo2">Number of Peering ASNs visible in one or more IXPs</p>     
                        <p id="subtitulo">Over the last 12 months</p>
                    </div>
                    <div id="piechart12" style="width: 550px; height: 350px; float: left;"></div>
                </div>   
            </div>
        </div>
        <div id="separador"></div>
        <div id="separador"></div>
        <div style="width: 1300px; height: 375px; margin-left:0px;">
                <div id="primero_2" style="width: 550px; height: 400px; margin-left:30px; display: inline-block;">
                    <div id="parrafos">
                        <p class ="titulo" id="titulo1">Number of Peering ASNs visible in one or more IXPs</p>     
                        <p id="subtitulo1">Over the last year</p>
                    </div>
                    <div id="piechart22" style="width: 550px; height: 350px; float: left;"></div>
                </div>
                <div id="segundo_2" style="width: 550px; height: 400px; margin-left:30px; display: inline-block;">
                    <div id="parrafos">
                        <p class="titulo" id="titulo2">Number of Peering ASNs visible in one or more IXPs</p>     
                        <p id="subtitulo2">Over the last year</p>
                    </div>
                    <div id="piechart21" style="width: 550px; height: 350px; float: left;"></div>
                </div>   
            </div>
        </div>
        <div id="separador2"></div>
        <div id="separador2"></div>
        
        <div style="width: 1300px; height: 375px; margin-left:0px;">
                <div id ="select">
                    <select name="selectYear" id='selectYear' onFocus='chargeList();' onClick='paint()'>
                        <option>Select Year :</option>
                    </select>
    
                </div>
                <div id="primero_2" style="width: 550px; height: 400px; margin-left:340px; display: inline-block;">
                    <div id="parrafos">
                        <p class ="titulo" id="titulo1">Number of Peering ASNs visible in one or more IXPs</p>     
                        <p id="subtitulo3">Over the last year</p>
                    </div>
                    <div id="piechart3" style="width: 550px; height: 350px; float: left;"></div>
                </div>
            </div>
        </div>
       
    </body>
</html>

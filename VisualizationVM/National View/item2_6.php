<html>
    <head>
        <link rel="stylesheet" href="css/select.css">
        <?php
            ini_set('memory_limit', '-1');

            $lastMonthASNs = array();
            
            if (file_exists('outputs_Regional_View/17_Number_ASNs_peering_at_IXP_visible_in_BGP_data_lastmonth/LastMonth__infos_peering_ASNs.txt') == 0) {
                $file = fopen('outputs_Regional_View/17_Number_ASNs_peering_at_IXP_visible_in_BGP_data_lastmonth/LastMonth__infos_peering_ASNs.txt', "w");
                fwrite($file, "" . PHP_EOL);
                fclose($file);
            }
            $fileOpen = fopen('outputs_Regional_View/17_Number_ASNs_peering_at_IXP_visible_in_BGP_data_lastmonth/LastMonth__infos_peering_ASNs.txt','r');
            if (!$fileOpen){
                echo 'ERROR: No ha sido posible abrir el archivo. Revisa su nombre y sus permisos.'; exit;
            }

            $index = 0; // contador de líneas
            while (!feof($fileOpen)) { // loop hasta que se llegue al final del archivo
                $line = trim(fgets($fileOpen)); // guardamos toda la línea en $line como un string
                if (strpos($line, 'Number of ASNs assigned by Afrinic ;') !== false){
                    $list[$index] = explode(";",$line);
                    $index++;
                }
                if (strpos($line, 'Number of ASNs assigned by Afrinic peering at an African IXP ;') !== false){
                    $list[$index] = explode(";",$line);
                    $index++;
                }
                $fileOpen++; // necesitamos llevar el puntero del archivo a la siguiente línea
            }
            
            $list2 = array();
            for ($j=0; $j < count($list); $j++) {
                  if (strpos($list[$j][0], 'Number of ASNs assigned by Afrinic peering at an African IXP ') !== false){
                    $list2[$j][0] = 'ASNs Directly Peering at an African IXPs';
                }else{
                    $list2[$j][0] = 'ASNs NOT Directly Peering at any African IXP';
                }
                $list2[$j][1] = intval($list[$j][1]);
            }
            $lastMonthASNs = $list2;

            $lastMonthASNs2 = array();
            
            if (file_exists('outputs_Regional_View/18_Number_Origin_ASNs_visible_in_BGP_data_lastmonth//LastMonth__infos_Origin_ASNs.txt') == 0) {
                $file = fopen('outputs_Regional_View/18_Number_Origin_ASNs_visible_in_BGP_data_lastmonth//LastMonth__infos_Origin_ASNs.txt', "w");
                fwrite($file, "" . PHP_EOL);
                fclose($file);
            }
            $fileOpen = fopen('outputs_Regional_View/18_Number_Origin_ASNs_visible_in_BGP_data_lastmonth//LastMonth__infos_Origin_ASNs.txt','r');
            if (!$fileOpen){
                echo 'ERROR: No ha sido posible abrir el archivo. Revisa su nombre y sus permisos.'; exit;
            }

            $index = 0; // contador de líneas
            while (!feof($fileOpen)) { // loop hasta que se llegue al final del archivo
                $line = trim(fgets($fileOpen)); // guardamos toda la línea en $line como un string
                if (strpos($line, 'Number of ASNs assigned by Afrinic ;') !== false){
                    $list[$index] = explode(";",$line);
                    $index++;
                }
                if (strpos($line, 'Number of Origin ASNs assigned by Afrinic visibles at an African IXP ;') !== false){
                    $list[$index] = explode(";",$line);
                    $index++;
                }
                $fileOpen++; // necesitamos llevar el puntero del archivo a la siguiente línea
            }
            
            $list2 = array();
            for ($j=0; $j < count($list); $j++) {
                if (strpos($list[$j][0], 'Number of Origin ASNs assigned by Afrinic visibles at an African IXP') !== false){
                    $list2[$j][0] = 'Origin ASNs visible at African IXPs';
                }else{
                    $list2[$j][0] = 'Origin ASNs NOT visible at any African IXP';
                }
                
                $list2[$j][1] = intval($list[$j][1]);
            }
            $lastMonthASNs2 = $list2;

            ?>

        <script type="text/javascript" src="//cdnjs.cloudflare.com/ajax/libs/jquery/2.0.3/jquery.min.js"></script>
        <script type="text/javascript" src="https://www.google.com/jsapi"></script>
        <script type="text/javascript">
     
            google.load("visualization", "1", {packages:["geochart","corechart"]});
            google.setOnLoadCallback(init);

            var listIXP = (<?php echo json_encode($listIXP)?>);
            var percentage1 = (<?php echo json_encode($lastMonthASNs)?>);
            var percentage2 = (<?php echo json_encode($lastMonthASNs2)?>);
            
            percentage1[0][1] = percentage1[0][1] - percentage1[1][1];
            percentage2[0][1] = percentage2[0][1] - percentage2[1][1];  
    
            function init(){
                drawChart();
            }

            function paint(){
               
                drawChart();
            }
     
            function drawChart() {
       
                var data = new google.visualization.DataTable();

                data.addColumn('string', 'Country');
                data.addColumn('number', 'Percentage');

                data.addRows(percentage1);

                var options = {
                  'title':'ASNs',
                  is3D: false,
                  fontName: 'Trebuchet MS',
                  colors: ['#53A8FB', '#F1CA3A']
                };

                var chart = new google.visualization.PieChart(document.getElementById('piechart11'));
                google.visualization.events.addListener(chart, 'select', selectHandler);
                chart.draw(data, options);
                function selectHandler() {
                    var selectedItem = chart.getSelection()[0]
                    if (selectedItem.row == 0){
                         if (confirm("Do you want to download this file?") == true) {
                            downloadURI('outputs_Regional_View/17_Number_ASNs_peering_at_IXP_visible_in_BGP_data_lastmonth/List_ASNs_assigned_by_Afrinic.txt', 'List_of_ASNs_assigned_by_Afrinic.txt');
                        }
                        
                    }
                   if (selectedItem.row == 1) {
                        if (confirm("Do you want to download this file?") == true) {
                            downloadURI('outputs_Regional_View/17_Number_ASNs_peering_at_IXP_visible_in_BGP_data_lastmonth/List_ASNs_peering_at_an_African_IXP.txt', 'List_of_ASNs_assigned_by_Afrinic_peering_at_an_African_IXP.txt');
                        }

                    }
                }

                /*----------------------------------------------------------------------------*/

                var data2 = new google.visualization.DataTable();
        
                data2.addColumn('string', 'Region');
                data2.addColumn('number', 'Percentage');
                data2.addRows(percentage2);

                var options2 = {
                    'title':'ASNs',
                    is3D: false,
                    fontName: 'Trebuchet MS'
                };

                var chart2 = new google.visualization.PieChart(document.getElementById('piechart21'));
                google.visualization.events.addListener(chart2, 'select', selectHandler2);
                chart2.draw(data2, options2);
                function selectHandler2() {
                    var selectedItem = chart2.getSelection()[0]
                    if (selectedItem.row == 0){
                         if (confirm("Do you want to download this file?") == true) {
                            downloadURI('outputs_Regional_View/18_Number_Origin_ASNs_visible_in_BGP_data_lastmonth/List_ASNs_assigned_by_Afrinic.txt', 'List_of_ASNs_assigned_by_Afrinic.txt');
                        }
                        
                    }
                   if (selectedItem.row == 1) {
                        if (confirm("Do you want to download this file?") == true) {
                            downloadURI('outputs_Regional_View/18_Number_Origin_ASNs_visible_in_BGP_data_lastmonth/List_Origin_ASNs_at_an_African_IXP.txt', 'List_of_Origin_ASNs_assigned_by_Afrinic_visible_at_an_African_IXP.txt');
                        }

                    }
                    
                }
            }


            function downloadURI(uri,name) {
                var link = document.createElement("a");
                link.download = name;
                link.href = uri;
                link.click();
            }


            function descarga3(){
                console.log("adddd")
                var seleccionado = document.getElementById("selectIXP");
                var numero = seleccionado.selectedIndex;
                if (numero == 0) {
                    
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
          
            <div style="width: 1100px; height: 375px; margin-left:30px;">
                <div id="primero" style="width: 450px; height: 400px; margin-left:30px; display: inline-block;">
                    <div id="parrafos">
                        <p class ="titulo" id="titulo1">Percentage of Peering ASNs</p>     
                        <p id="subtitulo">Over the last month</p>
                    </div>
                    <div id="piechart11" style="width: 550px; height: 350px; float: left;"></div>
                </div>
                <div id="segundo" style="width: 450px; height: 400px; margin-left:30px; display: inline-block;">
                    <div id="parrafos">
                        <p class="titulo" id="titulo2">Percentage of Origin ASNs</p>     
                        <p id="subtitulo">Over the last month</p>
                    </div>
                    <div id="piechart21" style="width: 550px; height: 350px; float: left;"></div>
                </div>   
            </div>
        </div>
  </body>
</html>
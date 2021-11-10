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
            
            $percentageIPv4 = array();

            //Txt in to an array
            $fileOpen = fopen('outputs_National_View/7_percentage_IP_blocks_assigned_to_country_visible_at_IXP/Percentage_IPv4_assigned_to_country_appearing_per_CC/Infos_IPblocks_per_country.txt','r');
            if (!$fileOpen){
                echo 'ERROR: No ha sido posible abrir el archivo. Revisa su nombre y sus permisos.'; exit;
            }
            $index = 0; // contador de líneas
            while (!feof($fileOpen)) { // loop hasta que se llegue al final del archivo
                $line = trim(fgets($fileOpen)); // guardamos toda la línea en $line como un string
                $percentageIPv4[$index] = explode(";",$line);
                $fileOpen++; // necesitamos llevar el puntero del archivo a la siguiente línea
                $index++;
            }
            
            $percentageIPv4_2 = array();
            for ($i=1; $i < count($percentageIPv4)-1; $i++) { 
                $percentageIPv4_2[$i-1][0] = $percentageIPv4[$i][1];
                $percentageIPv4_2[$i-1][1] = intval($percentageIPv4[$i][3]);
                $percentageIPv4_2[$i-1][2] = intval($percentageIPv4[$i][4]);
            }
            $percentageIPv4 = $percentageIPv4_2;

            $percentageIPv6 = array();

            //Txt in to an array
            $fileOpen = fopen('outputs_National_View/7_percentage_IP_blocks_assigned_to_country_visible_at_IXP/Percentage_IPv6_assigned_to_country_appearing_per_CC/Infos_IPblocks_per_country.txt','r');
            if (!$fileOpen){
                echo 'ERROR: No ha sido posible abrir el archivo. Revisa su nombre y sus permisos.'; exit;
            }

            $index = 0; // contador de líneas
            while (!feof($fileOpen)) { // loop hasta que se llegue al final del archivo
                $line = trim(fgets($fileOpen)); // guardamos toda la línea en $line como un string
                $percentageIPv6[$index] = explode(";",$line);
                $fileOpen++; // necesitamos llevar el puntero del archivo a la siguiente línea
                $index++;
            }

            $percentageIPv6_2 = array();
            for ($i=1; $i < count($percentageIPv6)-1; $i++) { 
                $percentageIPv6_2[$i-1][0] = $percentageIPv6[$i][1];
                $percentageIPv6_2[$i-1][1] = intval($percentageIPv6[$i][3]);
                $percentageIPv6_2[$i-1][2] = intval($percentageIPv6[$i][4]);
            }
            $percentageIPv6 = $percentageIPv6_2;


            ?>

        <script type="text/javascript" src="//cdnjs.cloudflare.com/ajax/libs/jquery/2.0.3/jquery.min.js"></script>
        <script type="text/javascript" src="https://www.google.com/jsapi"></script>
        <script type="text/javascript">
     
            google.load("visualization", "1", {packages:["geochart","corechart"]});
            google.setOnLoadCallback(init);

            var listIXP = (<?php echo json_encode($listIXP)?>);
            var listCC = (<?php echo json_encode($listCC)?>);
            var percentage1 = (<?php echo json_encode($percentageIPv4)?>);
            var percentage2 = (<?php echo json_encode($percentageIPv6)?>);
            var porcentaje1 = [];
            var porcentaje2 = [];
            var charge = 0;
    
            function init(){
                document.getElementById("titulo1").innerHTML = "Percentage of IPv4 blocks visibles at "+listCC[0][0];
                document.getElementById("titulo2").innerHTML = "Percentage of IPv6 blocks visibles at "+listCC[0][0];
                formatoCorrecto();
                drawChart(0);
            }

            function paint(){
                var seleccionado = document.getElementById("selectIXP");
                var numero = seleccionado.selectedIndex;
                if (numero == 0) {
                    numero = 1;
                };
                var valor = seleccionado.value;
                document.getElementById("titulo1").innerHTML = "Percentage of IPv4 blocks visibles at "+listCC[numero-1][0];
                document.getElementById("titulo2").innerHTML = "Percentage of IPv6 blocks visibles at "+listCC[numero-1][0];
                drawChart(numero-1);
            }
     
            function drawChart(i) {
       
                var data = new google.visualization.DataTable();

                data.addColumn('string', 'Country');
                data.addColumn('number', 'Percentage');

                data.addRows(porcentaje1[i]);

                var options = {
                  'title':'Prefixes',
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
                            downloadURI('outputs_National_View/7_percentage_IP_blocks_assigned_to_country_visible_at_IXP/Percentage_IPv4_assigned_to_country_appearing_per_CC/List_prefixes_assigned_advertised_'+listCC[i][0]+'.txt','IPv4_'+listCC[i][0]+'.txt');
                        }
                        /*var value = data2.getValue(selectedItem.row,0);
                        console.log('WE have here: '+value)
                        var find = ' ';
                        var re = new RegExp(find, 'g');
                        value = value.replace(re, "_");
                        value = value.substring(value.lastIndexOf("to_")+3,value.lastIndexOf("_seen"));
                        console.log('WE have'+value)*/
                    }
                   if (selectedItem.row == 1) {
                        if (confirm("Do you want to download this file?") == true) {
                            downloadURI('outputs_National_View/7_percentage_IP_blocks_assigned_to_country_visible_at_IXP/Percentage_IPv4_assigned_to_country_appearing_per_CC/List_prefixes_assigned_advertised_'+listCC[i][0]+'.txt','IPv4_'+listCC[i][0]+'.txt');
                        }
                        /*var value = data2.getValue(selectedItem.row,0);
                        console.log('WE have here: '+value)
                        var find = ' ';
                        var re = new RegExp(find, 'g');
                        value = value.replace(re, "_");
                        value = value.substring(value.lastIndexOf("to_")+3,value.lastIndexOf("_not_seen"));
                        console.log('WE have'+value)*/
                    }
                    /*if (confirm("Do you want to download this file?") == true) {
                        downloadURI('outputs_National_View/7_percentage_IP_blocks_assigned_to_country_visible_at_IXP/Percentage_IPv4_assigned_to_country_appearing_per_CC/List_prefixes_assigned_advertised_'+listIXP[i]+'.txt','IPv4_'+listIXP[i]+'.txt');
                    }*/
                }

                /*----------------------------------------------------------------------------*/

                var data2 = new google.visualization.DataTable();
        
                data2.addColumn('string', 'Region');
                data2.addColumn('number', 'Percentage');
                data2.addRows(porcentaje2[i]);

                var options2 = {
                    'title':'Prefixes',
                    is3D: false,
                    fontName: 'Trebuchet MS'
                };

                var chart2 = new google.visualization.PieChart(document.getElementById('piechart21'));
                google.visualization.events.addListener(chart2, 'select', selectHandler2);
                chart2.draw(data2, options2);
                function selectHandler2() {
                    var selectedItem = chart2.getSelection()[0];
                    if (selectedItem.row == 0) {
                        if (confirm("Do you want to download this file?") == true) {
                            downloadURI('outputs_National_View/7_percentage_IP_blocks_assigned_to_country_visible_at_IXP/Percentage_IPv6_assigned_to_country_appearing_per_CC/List_prefixes_assigned_advertised_'+listCC[i][0]+'.txt','IPv6_'+listCC[i][0]+'.txt');
                        }
                        /*var value = data2.getValue(selectedItem.row,0);
                        console.log('WE have here: '+value)
                        var find = ' ';
                        var re = new RegExp(find, 'g');
                        value = value.replace(re, "_");
                        value = value.substring(value.lastIndexOf("to_")+3,value.lastIndexOf("_seen"));
                        console.log('WE have'+value)*/
                    }
                    if (selectedItem.row == 1) {
                        if (confirm("Do you want to download this file?") == true) {
                            downloadURI('outputs_National_View/7_percentage_IP_blocks_assigned_to_country_visible_at_IXP/Percentage_IPv6_assigned_to_country_appearing_per_CC/List_prefixes_assigned_advertised_'+listCC[i][0]+'.txt','IPv6_'+listCC[i][0]+'.txt');
                        }
                        /*var value = data2.getValue(selectedItem.row,0);
                        console.log('WE have here: '+value)
                        var find = ' ';
                        var re = new RegExp(find, 'g');
                        value = value.replace(re, "_");
                        value = value.substring(value.lastIndexOf("to_")+3,value.lastIndexOf("_not_seen"));
                        console.log('WE have'+value)*/
                    }
                    /*if (confirm("Do you want to download this file?") == true) {
                        downloadURI('outputs_National_View/7_percentage_IP_blocks_assigned_to_country_visible_at_IXP/Percentage_IPv6_assigned_to_country_appearing_per_CC/List_prefixes_assigned_advertised_'+listIXP[i]+'.txt','IPv6_'+listIXP[i]+'.txt');
                    }*/
                    
                }
            }

            
            function formatoCorrecto(){
                aux = 'fuera'
                for (var i = 0; i < listCC.length; i++) {
                    aux = 'fuera'
                    auxiliar1 = [['IPv4 blocks \n assigned to '+listCC[i][0]+' seen at '+listCC[i][0],0],['IPv4 blocks \n assigned to '+listCC[i][0]+' not seen at '+listCC[i][0],0]];
                    for (var j = 0; j < percentage1.length; j++) {
                        if(percentage1[j][0].trim() == listCC[i][0].trim()){
                            auxiliar1[0][1] = percentage1[j][1];
                            auxiliar1[1][1] = percentage1[j][2]-percentage1[j][1];
                            j=300;
                            aux = 'dentro'
                            porcentaje1.push(auxiliar1);
                        }
                    };
                    if (aux == 'fuera') {
                        auxiliar1[0][1] = 0;
                        auxiliar1[1][1] = 0;
                        porcentaje1.push(auxiliar1);
                    };
                };

                 for (var i = 0; i < listCC.length; i++) {
                    aux = 'fuera'
                    auxiliar1 = [['IPv6 blocks \n assigned to '+listCC[i][0]+' seen at '+listCC[i][0],0],['IPv6 blocks \n assigned to '+listCC[i][0]+' not seen at '+listCC[i][0],0]];
                    for (var j = 0; j < percentage2.length; j++) {
                        if(percentage2[j][0].trim() == listCC[i][0].trim()){
                            auxiliar1[0][1] = percentage2[j][1];
                            auxiliar1[1][1] = percentage2[j][2]-percentage2[j][1];
                            j=300;
                            aux = 'dentro'
                            porcentaje2.push(auxiliar1);
                        }
                    };
                    if (aux == 'fuera') {
                        auxiliar1[0][1] = 0;
                        auxiliar1[1][1] = 0;
                        porcentaje2.push(auxiliar1);
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
                    <option>Select Country:</option>
                </select>
    
            </div>

            <div style="width: 1100px; height: 375px; margin-left:30px;">
                <div id="primero" style="width: 450px; height: 400px; margin-left:30px; display: inline-block;">
                    <div id="parrafos">
                        <p class ="titulo" id="titulo1"></p>     
                        <p id="subtitulo">Over the last month</p>
                    </div>
                    <div id="piechart11" style="width: 550px; height: 350px; float: left;"></div>
                </div>
                <div id="segundo" style="width: 450px; height: 400px; margin-left:30px; display: inline-block;">
                    <div id="parrafos">
                        <p class="titulo" id="titulo2"></p>     
                        <p id="subtitulo">Over the last month</p>
                    </div>
                    <div id="piechart21" style="width: 550px; height: 350px; float: left;"></div>
                </div>   
            </div>
        </div>
  </body>
</html>
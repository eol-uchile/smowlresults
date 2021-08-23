/* Javascript for SMOWLRESULTS*/
function IframeWithAnonymousIDXBlock(runtime, element, settings) {
    $(function ($) {
        if (settings.has_settings){
            var nombre = settings.nomExamenes;
            if(nombre==="")
            {
                $(element).find('#ocultarDiv')[0].style.display = "none";
                //document.getElementById("ocultarDiv").style.display = "none";
            }
            else
            {
                var tamE = settings.tamExamenes;
                var nombre2 = nombre.split(",");

                //var select = document.getElementById('listaEx');
                var select = $(element).find('#listaEx')[0];
                var opt = document.createElement('option');
                opt.value = "Empty";
                opt.text =  "--Select--";
                select.appendChild(opt);

                for(var i = 0; i<tamE; i++)
                {
                    opt = document.createElement('option');
                    var nombrePunto = nombre2[i].split(".");
                    opt.value = nombrePunto[0];
                    opt.text =  nombrePunto[1];
                    select.appendChild(opt);
                }

                function seleccionar(sel)
                {
                    var val = sel.options[sel.selectedIndex].value;
                    var txt3 = sel.options[sel.selectedIndex].text;
                    var txt2 = txt3.split(" ").join("_");

                    if(val !="Empty" )
                    {
                        $(element).find('input[name="idCourse"]')[0].value = val;
                        $(element).find('input[name="course_MoodleName"]')[0].value = txt2;
                        //document.getElementsByName("idCourse")[0].value = val;
                        //document.getElementsByName("course_MoodleName")[0].value = txt2;
                        //var ifra = document.getElementById("smowl");
                        var ifra = $(element).find('#smowl')[0];
                        ifra.style.minHeight = '500px';
                        ifra.style.height = 'auto';
                        //ifra.height = "3374";
                        ifra.width = "105%";

                        //var resultsForm2 = document.getElementById("resultsForm");
                        var resultsForm2 = $(element).find('#resultsForm')[0];
                        resultsForm2.style.display = "inline";
                        resultsForm2.submit();
                    }
                    else
                    {
                        var ifra = $(element).find('#smowl')[0];
                        ifra.style.minHeight = '0';
                        ifra.style.height = '0';
                        //ifra.height = "0";
                        ifra.width = "0";
                    }
                }
            }
        }
    });
}

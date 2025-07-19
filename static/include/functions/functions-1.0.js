
/**
 * Utilizzata da formatNumber per inserire i separatori delle migliaia.
 * @param nStr
 * @returns {string}
 */
function addCommas(nStr) {
    nStr += '';
    var x = nStr.split(',');
    var x1 = x[0];
    var x2 = x.length > 1 ? ',' + x[1] : '';
    var rgx = /(\d+)(\d{3})/;
    while (rgx.test(x1)) {
        x1 = x1.replace(rgx, '$1' + '.' + '$2');
    }
    return x1 + x2;
}

/**
 * Formatta i numeri in formato italiano, con la virgola come separatore dei decimali.
 * Accetta 3 parametri: il numero da formattare (senza precedenti formattazioni, in formato #0.00),
 * fixed: quante cifre dopo la virgola tenere,
 * commas: se 1 utilizza i punti come separatore delle migliaia.
 * @param number numero da formattare
 * @param fixed numero di cife dopo la virgola
 * @param commas 1: punti come separatori delle migliaia, 0: nessun punto
 * @returns {string|*} una stringa contenente il numero formattato.
 */
function formatNumber(number, fixed, commas) {
    if (Number.isNaN(parseInt(number))) {
        return '';
    }

    number = parseFloat(number).toFixed(fixed).toString().replace(".", ",");
    if(commas)
        return addCommas(number);
    else
        return number;
}

function resizeJQGrid(grid_id) {
    var $grid = $('#' + grid_id);
    var $container = $grid.parents('#gbox_' + grid_id).parent();
    if ($container.size() > 0 && $container.is(':visible')) {
        var width = $container.width();
        $grid.jqGrid('setGridWidth', width);
    }
}

function checkAjaxResponse(response, redir) {
    message = false;

    if (response.success === false)
    {
        showError('Attenzione', "Errore", '<button class="btn btn-primary" data-dismiss="modal" type="button">Chiudi</button>');
        return 1;
    }

    if (message) {
        response = $.trim(response);

        if (response == 0 || response == 1 || response == 2 || response == 3 || response == 4 || response == 5 || response == 10) {
            // Errori lato DB
            if (redir) {
                $('<div>Internal Server Error</div>').dialog({
                    modal: true,
                    title: message_title,
                    buttons: [{
                        text: 'OK',
                        click: function () {
                            $(this).dialog('close');
                        }
                    }],
                    close: function (event, ui) {
                        $(this).dialog('destroy');
                        $(this).remove();
                    }
                });
            } else {
                return return_values.db_error;
            }
        } else if (response == 7 || response == 9 || response == 13 || response == 14) {
            // Sessione scaduta
            if (redir) {
                redirect(BASE_URL, 'err=undefined_session', false);
            } else {
                return return_values.session_error;
            }
        } else if (response == 12) {
            // Mancanza di permessi
            if (redir) {
                redirect(BASE_URL, 'err=no_permission', false);
            } else {
                return return_values.no_permission;
            }
        } else {
            if (redir) {
                showError('Attenzione', response, '<button class="btn btn-primary" data-dismiss="modal" type="button">Chiudi</button>');
            } else {
                return response;
            }
        }
    }

    return 0;
}

function checkSelectOption(value) {
    console.log(value);
    if (value == '') {
        return [false, 'Please, select an option'];
    } else {
        return [true, ''];
    }
}

function redirect(url, params, redirect) {
    if (typeof url == 'undefined') url = BASE_URL;

    if (typeof params == 'undefined') {
        params = '';
    } else {
        params = '?' + params;
    }

    if (typeof redirect != 'undefined' && redirect) {
        params += '&redirect_url=' + window.location;
    }

    window.location.replace(url + params);
}


function isHostValid(value, colname) {

    if (value == "localhost" || value == "")
        return [true, ""];

    var re1='((?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))(?![\\d])';	// IPv4 IP Address 1

    var myRegex1 = new RegExp(re1,["i"]);
    var res = myRegex1.exec(value);
    if (res != null)
        return [true, ""];

    var re2='((?:http|https)(?::\\/{2}[\\w]+)(?:[\\/|\\.]?)(?:[^\\s"]*))';	// HTTP URL 1

    var myRegex2 = new RegExp(re2,["i"]);
    res = myRegex2.exec(value);
    if (res != null)
        return [true, ""];


    var re3='((?:\\/[\\w\\.\\-]+)+)';	// Unix Path 1
    var myRegex3 = new RegExp(re3,["i"]);
    res = myRegex3.exec(value);
    if (res != null) {
        return [true, ""];
    } else {
        return [false, colname + ": Insert an IP, HTTP URL or Unix Path"]
    }
}

function randomIntFromInterval(min,max)
{
    return Math.floor(Math.random()*(max-min+1)+min);
}


function showError(title, body, footer, islocking) {
    if (islocking === undefined) {
        islocking = false;
    }
    $('#error-title').html(title);
    $('#error-body').html(body);
    $('#error-footer').html(footer);
    $("#error-modal").modal('show');
}

function showToast(body, footer, islocking) {
    if (islocking === undefined) {
        islocking = false;
    }
    //$('#toast-header').html(title);
    $('#toast-body').html(body);
    bsAlert.show();
}

/**
 *
 * @param canvas
 * @param percent_gauge_value
 * @param style dark/light
 */
function drawGauge(canvas, percent_gauge_value, style='dark') {
    let rect =  canvas.getBoundingClientRect();

    var blue_color = 'rgb(0, 120, 187)';
    var white_color = 'rgb(255, 255, 255)';
    var back_color = '#3A416F';

    var black_color = 'rgb(0, 0, 0)';
    canvas.width = rect.width*2;
    canvas.height = rect.height*2;
    canvas.style.width = rect.width + 'px';
    canvas.style.height = (rect.height) + 'px';

    let elementColorPrimary = black_color;
    let elementColorSecondary = white_color;
    let canvas_color = white_color;
    if(style == 'dark') {
        elementColorPrimary = white_color;
        elementColorSecondary = black_color;
        canvas_color = '#141727';
    }

    origin_x = canvas.width / 2;
    origin_y = canvas.height - 20;

    let ctx = canvas.getContext('2d', {
        alpha: true
    });
    ctx.translate(0.5, 0.5);

    ctx.clearRect(0, 0, canvas.width, canvas.height); // clear canvas
    ctx.fillStyle = canvas_color;
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    let gaugeGradient = ctx.createConicGradient(Math.PI / 2, origin_x, origin_y);

    gaugeGradient.addColorStop(0.25, '#82D616');
    gaugeGradient.addColorStop(0.48, '#82D616');
    gaugeGradient.addColorStop(0.51, '#FBCF33');
    gaugeGradient.addColorStop(0.62, '#FBCF33');
    gaugeGradient.addColorStop(0.67, '#D1002E');
    gaugeGradient.addColorStop(0.70, '#D1002E');

    stroke_width = canvas.height * 0.1;
    radius_external = canvas.width / 2 - canvas.width * 0.05-20;

    pointer_circle_internal = 1;
    pointer_circle_width_internal = canvas.width * 0.01;

    pointer_circle_external = canvas.width * 0.02;
    pointer_circle_width_external = canvas.width * 0.01;

    pointer_triangle_width = pointer_circle_external * 1.1;
    pointer_triangle_height = radius_external * 0.5;

    ctx.save();

    ctx.translate(origin_x, origin_y);
    ctx.rotate(-Math.PI / 2 + Math.PI * percent_gauge_value);
    // Disegna icona potenza
    let power_icon_image = new Image();
    power_icon_image.src = 'img/power_gauge_icon.png';
    power_icon_image.onload = function(){

        ctx.drawImage(power_icon_image, origin_x-(power_icon_image.width/2), origin_y - canvas.height/2+10);
    }
    // Disegna Lancetta
    drawTriangle(ctx, 0, 0, pointer_triangle_width, pointer_triangle_height, elementColorPrimary);
    drawCircle(ctx, 0, 0, pointer_circle_external, elementColorPrimary, pointer_circle_width_external, elementColorSecondary);
    ctx.restore();
    // Disegna le lineette
    let font_text = '20pt Open Sans';
    let origin_y_t = origin_y - 1;
    let positionText_0 = [];
    let positionText_50 = [origin_x, origin_y_t - (radius_external * 0.7)];
    let positionText_80 = [];
    let positionText_100 = [];

    for (var i = 0; i < 6; i++) {
        alfa = Math.PI / 10 * i;
        inizio_x = origin_x - (radius_external * 0.8 * Math.sin(alfa));
        fine_x = origin_x - (radius_external * Math.sin(alfa));
        inizio_y = origin_y_t - (radius_external * 0.8 * Math.cos(alfa));
        fine_y = origin_y_t - (radius_external * Math.cos(alfa));

        text_x = origin_x - (radius_external * 0.7 * Math.sin(alfa));
        text_y = origin_y_t - (radius_external * 0.7 * Math.cos(alfa));

        if (i == 5) {
            positionText_0 = [text_x, text_y];
        }

        drawLine(ctx, inizio_x, inizio_y, fine_x, fine_y, back_color, 3);
        inizio_x = origin_x + (radius_external * 0.8 * Math.sin(alfa));
        fine_x = origin_x + (radius_external * Math.sin(alfa));
        inizio_y = origin_y_t - (radius_external * 0.8 * Math.cos(alfa));
        fine_y = origin_y_t - (radius_external * Math.cos(alfa));
        drawLine(ctx, inizio_x, inizio_y, fine_x, fine_y, back_color, 3);

        text_x = origin_x + (radius_external * 0.7 * Math.sin(alfa));
        text_y = origin_y_t - (radius_external * 0.7 * Math.cos(alfa));

        if (i == 5) {
            positionText_100 = [text_x - 10, text_y];
        } else if (i == 3) {
            positionText_80 = [text_x - 10, text_y];
        }

    }

    drawText(ctx, font_text, elementColorPrimary, positionText_0[0], positionText_0[1], "0");
    drawText(ctx, font_text, elementColorPrimary, positionText_50[0], positionText_50[1], "50");
    drawText(ctx, font_text, elementColorPrimary, positionText_80[0], positionText_80[1], "80");
    drawText(ctx, font_text, elementColorPrimary, positionText_100[0], positionText_100[1], "100");

    for (var i = 0; i < 11; i++) {
        alfa = Math.PI / 20 * i;
        inizio_x = origin_x - (radius_external * 0.87 * Math.sin(alfa));
        fine_x = origin_x - (radius_external * Math.sin(alfa));
        inizio_y = origin_y_t - (radius_external * 0.87 * Math.cos(alfa));
        fine_y = origin_y_t - (radius_external * Math.cos(alfa));
        drawLine(ctx, inizio_x, inizio_y, fine_x, fine_y, back_color, 2);
        inizio_x = origin_x + (radius_external * 0.87 * Math.sin(alfa));
        fine_x = origin_x + (radius_external * Math.sin(alfa));
        inizio_y = origin_y_t - (radius_external * 0.87 * Math.cos(alfa));
        fine_y = origin_y_t - (radius_external * Math.cos(alfa));
        drawLine(ctx, inizio_x, inizio_y, fine_x, fine_y, back_color, 2);
    }

    // Disegna Arco
    drawHalfCircle(ctx, origin_x, origin_y, radius_external, back_color, stroke_width, 1);
    drawHalfCircle(ctx, origin_x, origin_y, radius_external, gaugeGradient, stroke_width, percent_gauge_value);
}

function drawLine(ctx, start_x, start_y, end_x, end_y, stroke_color, stroke_width) {
    ctx.beginPath();
    ctx.lineWidth = stroke_width;
    ctx.fillStyle = "rgba (0, 0, 0, 0)"; // transparent
    ctx.strokeStyle = stroke_color;
    ctx.moveTo(start_x, start_y);
    ctx.lineTo(end_x, end_y);
    ctx.stroke();
}

function drawHalfCircle(ctx, x, y, radius, stroke_color, stroke_width, percent_drawn) {
    ctx.beginPath();
    ctx.lineWidth = stroke_width;
    ctx.fillStyle = "rgba (0, 0, 0, 0)"; // transparent
    ctx.strokeStyle = stroke_color;
    ctx.arc(x, y, radius, Math.PI, Math.PI + Math.PI * percent_drawn, false);
    ctx.stroke();
}

function drawCircle(ctx, x, y, radius, stroke_color, stroke_width, fill_color) {
    ctx.beginPath();
    ctx.lineWidth = stroke_width;
    ctx.fillStyle = fill_color; // transparent
    ctx.strokeStyle = stroke_color;
    ctx.arc(x, y, radius, 0, Math.PI * 2, false);
    ctx.fill();
    ctx.stroke();
}

function drawTriangle(ctx, x, y, base, height, stroke_color) {
    ctx.fillStyle = stroke_color; // transparent
    ctx.strokeStyle = stroke_color;
    ctx.beginPath();
    ctx.moveTo(x - base / 2, y);
    ctx.lineTo(x, y - height);
    ctx.lineTo(x + base / 2, y);
    ctx.fill();
}

function drawText(ctx, font, color, x, y, text) {
    ctx.textBaseline = 'middle';
    ctx.textAlign = "center";
    ctx.font = font;
    ctx.fillStyle = color;
    ctx.fillText(text, x, y);
}


function updateTokenRequest() {
    setInterval(function () {
        jQuery.ajax({
            url: ajax_script + '?fun=refreshsession',
            type: 'POST',
            async: true,
            success: function (data) {
                if ((data = jQuery.trim(data)) == '') return;
                try {
                    var parsedResult = jQuery.parseJSON(data);
                    if (parsedResult != 100) {
                        window.location.replace("/?err=login_required");
                    }
                } catch (ex) {
                    window.location.replace("/?err=login_required");
                }
            }
        });
    }, 60000);
}


var language_selects = {
    errorLoading: function () {
        return 'I risultati non possono essere caricati.';
    },
    inputTooLong: function (args) {
        var overChars = args.input.length - args.maximum;

        var message = 'Per favore cancella ' + overChars + ' caratter';

        if (overChars !== 1) {
            message += 'i';
        } else {
            message += 'e';
        }

        return message;
    },
    inputTooShort: function (args) {
        var remainingChars = args.minimum - args.input.length;

        var message = 'Per favore inserisci ' + remainingChars + ' o più caratteri';

        return message;
    },
    loadingMore: function () {
        return 'Caricando più risultati…';
    },
    maximumSelected: function (args) {
        var message = 'Puoi selezionare solo ' + args.maximum + ' element';

        if (args.maximum !== 1) {
            message += 'i';
        } else {
            message += 'o';
        }

        return message;
    },
    noResults: function () {
        return 'Nessun risultato trovato';
    },
    searching: function () {
        return 'Sto cercando…';
    }
};

function debounce(fn, ms) {

    let timer
    return function(...args) {
        clearTimeout(timer)
        timer = setTimeout(fn.bind(this, ...args), ms || 0)
    }
}


function reinitTooltips() {
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));

}

function clearTooltips() {
    $('.tooltip').remove();
}
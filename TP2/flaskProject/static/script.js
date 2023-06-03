$(document).ready(function () {
    $('#dictionary-table').DataTable();
});


function deleteGlossaryTerm(term) {
    $("#glossary_" + term).html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Deleting...');

    $.ajax("/glossary/" + term, {
        type: "DELETE",
        success: function (data) {
            $("#glossary_" + term).remove();
            // mostrar a mensagem de sucesso
            showNotification('The term "' + term + '" was deleted successfully.', "alert-success");
            // window.location.href = '/glossary';
        },
        error: function (error) {
            // mostrar a mensagem de erro
            showNotification("Error deleting term: " + error, "alert-danger");
            console.error("Error deleting term: " + error);
        }
    });
}

function showNotification(message, alertClass) {

    $(".alert-notification").remove();
    var notification = $("<div>").addClass("alert " + alertClass + " alert-notification").text(message);
    $("#notifications-container").prepend(notification);

    // Remover a notificação após 3 segundos (3000 milissegundos)
    setTimeout(function () {
        notification.remove();
    }, 2000);
}

function editGlossaryTerm(term) {
    // Redirecionar para a rota de edição do termo
    window.location.href = '/glossary/edit/' + term;
}

function showTranslation(lang, description) {
    const translationElement = document.querySelector('.card-translation');
    translationElement.style.display = 'block';
    const langElement = translationElement.querySelector('.lang');
    langElement.innerHTML = lang.toUpperCase() + ' <span class="flag-icon flag-icon-' + lang + '"></span>';
    const translation = translationElement.querySelector('.translation');
    translation.textContent = description;
}

function addTranslationRow() {
    var newRow = document.createElement('tr');
    newRow.classList.add("translation-row");
    newRow.innerHTML = `
        <td contenteditable="true" class="language-cell"></td>
        <td contenteditable="true" class="translation-cell"></td>
        <td>
            <button type="button" class="btn btn-sm" onclick="removeTranslationRow(this)"><i class="bi bi-trash"></i></button>
        </td>
    `;
    document.getElementById('translations-table-body').appendChild(newRow);
}


function removeTranslationRow(button) {
    var row = button.parentNode.parentNode;
    row.remove();
}

const glossaryForm = document.getElementById('glossary-form-edit');
if (glossaryForm) {
  glossaryForm.addEventListener('submit', function(event) {
    event.preventDefault();
    var term = glossaryForm.getAttribute('data-term');

    // Resto do código do handleSubmit
    var syn = document.getElementById('syn').value;
    var descr = document.getElementById('descr').value;
    var tag = document.getElementById('tag').value;

    var translations = {};
    var translationRows = document.getElementsByClassName('translation-row');
    for (var i = 0; i < translationRows.length; i++) {
        var languageCell = translationRows[i].querySelector('.language-cell');
        var translationCell = translationRows[i].querySelector('.translation-cell');
        var language = languageCell.textContent.trim();
        var translation = translationCell.textContent.trim();
        translations[language] = translation;
    }

    var formData = {
        syn: syn,
        descr: descr,
        tag: tag,
        i18n: translations
    };

    $("#glossary-save-button").html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Saving...');
    // Envia os dados para o servidor
   $.ajax({
        url:"/glossary/edit/" + term,
        type: "POST",
        contentType: 'application/json',
        data: JSON.stringify(formData),
        success: function (data) {
           window.location.href = '/glossary/' + term;
        },
        error: function (error) {
            // mostrar a mensagem de erro
            alert("Erro: " + error);
            console.error("Error editing term: " + error);
        }
    });
  });
}


// JavaScript mostrar o tooltip
window.addEventListener('DOMContentLoaded', function() {
    var boneLabels = document.querySelectorAll('.bone-label');
    boneLabels.forEach(function(label) {
        label.addEventListener('mouseenter', function() {
            var boneId = label.dataset.boneId;
            var description = document.querySelector('.bone-description[data-bone-id="' + boneId + '"]');
            description.style.display = 'block';
        });

        label.addEventListener('mouseleave', function() {
            var boneId = label.dataset.boneId;
            var description = document.querySelector('.bone-description[data-bone-id="' + boneId + '"]');
            description.style.display = 'none';
        });
    });
});

function goBack() {
    history.back();
}
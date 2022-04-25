function ShowHide() {
	if ($('#show_completed').is(':checked')) $('#completed').show()
	else $('#completed').hide()
}

$(document).on('click', '#check', function () {
	const id = $(this).attr('item')
	$.ajax({
		type: 'POST',
		url: `/complete/${id}`,
		success: function () {
			$('#completed').load(' #completed')
			$('#uncomplete').load(' #uncomplete')
		},
	})
})

$(document).on('click', '#delete', function () {
	const id = $(this).attr('item')
	$.ajax({
		type: 'POST',
		url: `/delete/${id}`,
		success: function () {
			$('#completed').load(' #completed')
			$('#uncomplete').load(' #uncomplete')
		},
	})
})

$(document).on('submit', '#todo-form', function (e) {
	e.preventDefault()
	if ($('#todo').val()) {
		$.ajax({
			type: 'POST',
			url: '/',
			data: { description: $('#todo').val() },
			success: function () {
				$('#completed').load(' #completed')
				$('#uncomplete').load(' #uncomplete')
			},
		}).then(() => e.target.reset())
	}
})

$(document).on('submit', '#item-form', function (e) {
	e.preventDefault()
	const id = $(this).attr('item')
	if ($(`#item-${id}`).val()) {
		$.ajax({
			type: 'POST',
			url: `/edit/${id}`,
			data: { description: $(`#item-${id}`).val() },
			success: function () {
				$('#uncomplete').load(' #uncomplete')
			},
		})
	}
})

$(document).on('click', '#picker', function () {
	const id = $(this).attr('item')
	if ($(`#datepicker-${id}`).is(':visible')) {
		$(`#datepicker-${id}`).hide()
		$(`#date-${id}`).show()
	} else {
		$(`#date-${id}`).hide()
		$(`#datepicker-${id}`)
			.datepicker({
				onSelect: function (date) {
					const id = $(this).attr('item')
					$.ajax({
						type: 'POST',
						url: `/date/${id}`,
						data: { due_date: date },
						success: function () {
							$('#uncomplete').load(' #uncomplete')
						},
					})
				},
			})
			.show()
	}
})

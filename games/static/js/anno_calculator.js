var calculate_consumables = function() {
	var populations = {
		'farmer': Number($('#farmer-number').val()),
		'worker': Number($('#worker-number').val()),
		'artisan': Number($('#artisan-number').val()),
		'engineer': Number($('#engineer-number').val()),
		'investor': Number($('#investor-number').val())
	}

	for (var product in products) {
		var product_count = 0
		for (var consumer in products[product]) {
			product_count += populations[consumer] / products[product][consumer]
		}

		$product = $('#anno-product-' + product)
		if (product_count > 0) {
			$product.children('.anno-product-icon').removeClass('disabled')
			$product.children('.anno-product-name').removeClass('text-muted')
			$product.find('.anno-product-count').text(' x' + Math.ceil(product_count))
		}
		else {
			$product.children('.anno-product-icon').addClass('disabled')
			$product.children('.anno-product-name').addClass('text-muted')
			$product.find('.anno-product-count').text('')
		}
	}
}

$(function() {
	calculate_consumables()
})

$('.anno-population input').on('propertychange change keyup paste input', function() {
	calculate_consumables()
})

var products = {
	'fish': {
		'farmer': 800,
		'worker': 800
	},
	'workclothes': {
		'farmer': 650,
		'worker': 650
	},
	'schnapps': {
		'farmer': 600,
		'worker': 600
	},
	'sausages': {
		'worker': 1000,
		'artisan': 750
	},
	'bread': {
		'worker': 2200,
		'artisan': 1650
	},
	'soap': {
		'worker': 4800,
		'artisan': 3600
	},
	'beer': {
		'worker': 2600,
		'artisan': 1950
	},
	'cannedfood': {
		'artisan': 11700,
		'engineer': 7800
	},
	'sewingmachines': {
		'artisan': 4200,
		'engineer': 2800
	},
	'furcoats': {
		'artisan': 2250,
		'engineer': 1500
	},
	'rum': {
		'artisan': 2100,
		'engineer': 1400
	},
	'glasses': {
		'engineer': 9000,
		'investor': 5626
	},
	'coffee': {
		'engineer': 1700,
		'investor': 1062.5
	},
	'lightbulbs': {
		'engineer': 12800,
		'investor': 8000
	},
	'highwheelers': {
		'engineer': 6400,
		'investor': 4000
	},
	'pocketwatches': {
		'engineer': 20400,
		'investor': 12750
	},
	'champagne': {
		'investor': 4250
	},
	'cigars': {
		'investor': 9000
	},
	'chocolate': {
		'investor': 1875
	},
	'jewelry': {
		'investor': 9500
	},
	'gramophones': {
		'investor': 38000
	}
}

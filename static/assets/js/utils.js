function currencyFormatter({ currency, value}) {
  const formatter = new Intl.NumberFormat('es-MX', {
    style: 'currency',
    minimumFractionDigits: 2,
    currency
  })
  return formatter.format(value)
}

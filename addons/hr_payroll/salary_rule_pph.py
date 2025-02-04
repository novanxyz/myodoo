def rule(penghasilan_kena_pajak):

  pph_rate = [(60000000.0, 0.05), (250000000.0, 0.15), (50000000.0,0.25), (5000000000.0,0.3), (5000000001.0,0.35) ]
  result =0.0
  while penghasilan_kena_pajak > 0:
    print(penghasilan_kena_pajak, pph_rate)
    result += pph_rate[0][1] * min(pph_rate[0][0], penghasilan_kena_pajak)
    penghasilan_kena_pajak -= pph_rate[0][0]
    del pph_rate[0]

  return result



print(rule(80000000))

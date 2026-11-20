from datetime import datetime

ZILE_SAPTAMANA = [
    "Luni",
    "Marți",
    "Miercuri",
    "Joi",
    "Vineri",
    "Sâmbătă",
    "Duminică",
]

ZILE_ABRV = [
    "Lun",
    "Mar",
    "Mie",
    "Joi",
    "Vin",
    "Sâm",
    "Dum",
]

LUNI = [
    "Ianuarie",
    "Februarie",
    "Martie",
    "Aprilie",
    "Mai",
    "Iunie",
    "Iulie",
    "August",
    "Septembrie",
    "Octombrie",
    "Noiembrie",
    "Decembrie",
]

LUNI_ABRV = [
    "Ian",
    "Feb",
    "Mar",
    "Apr",
    "Mai",
    "Iun",
    "Iul",
    "Aug",
    "Sep",
    "Oct",
    "Noi",
    "Dec"
]

def formateaza_data(format: str = "%A, %d %B %Y, %H:%M:%S", data:datetime = datetime.now()) -> str:
  format = format.replace("%A", ZILE_SAPTAMANA[data.weekday()])
  format = format.replace("%B", LUNI[data.month - 1])
  format = format.replace("%a", ZILE_ABRV[data.weekday()])
  format = format.replace("%b", LUNI_ABRV[data.month - 1])
      
  return data.strftime(format)
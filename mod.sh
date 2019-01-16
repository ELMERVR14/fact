#!/bin/bash
sudo /etc/init.d/odooPERUSUNATADDON-server restart
sudo /etc/init.d/postgresql stop
sudo /etc/init.d/postgresql start
#sudo mv /home/rockscripts/.local/lib/python3.6/site-packages/xmlsec* /usr/local/lib/python3.6/dist-packages
#sudo /etc/init.d/odoo restart

##{"numero": "00000001", "tipoMoneda": "PEN", "receptor": {"tipo": 6, "direccion": "JR. MONTEROSA NRO. 233 INT. 904 (CHACARILLA DEL ESTANQUE)  LIMA", "nombre": "SALLY PERU HOLDINGS S.A.C.", "nro": "20549473301"}, "totalVenta": 7.6464, "emisor": {"ciudad": "LIMA", "tipo": 6, "direccion": "BENJAMIN FRANKLIN MZ. M LOT. 13", "departamento": "Chorrillos", "codigoPais": "PE", "codigoPostal": "15054","nombre": "Nekade", "nro": "20603408111"}, "serie": "F001", "sumatoriaIgv": "1.17", "fechaVencimiento": "2019-01-08", "totalVentaGravada": 6.48, "fechaEmision": "2019-01-08", "items": [{"cantidad":"1.0", "montoAfectacionIgv": 0.972, "tipoPrecioVentaUnitario": "01", "unidadMedidaCantidad": "ZZ", "valorUnitario": 5.4, "valorVenta": 5.4, "tipoAfectacionIgv": "10", "descripcion": "Ajos", "precioVentaUnitario": 6.372}, {"cantidad": "1.0", "montoAfectacionIgv": 0.19440000000000002, "tipoPrecioVentaUnitario": "01", "unidadMedidaCantidad": "ZZ", "valorUnitario": 1.08, "valorVenta": 1.08, "tipoAfectacionIgv": "10", "descripcion": "Apio", "precioVentaUnitario": 1.2744}], "horaEmision": "00:11:30"}
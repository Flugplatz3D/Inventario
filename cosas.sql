/*insert into clasificaciones (clasificacion) values ("prueba")

select * from clasificaciones

select * from detalles

select d.Descripcion, f.Clasificacion, d.Detalle, c.Caja, tc.TipoCaja , b.Bolsa, d.Cantidad, d.DetalleID
from detalles d, cajas c, bolsas b, clasificaciones f, TiposCaja tc 
where d.CajaID = c.CajaID  
and d.BolsaID = b.BolsaID 
and d.ClasificacionID = f.ClasificacionID 
and d.TipoCajaID = tc.TipoCajaID
ORDER BY upper(d.Descripcion) ASC

select t.TipoBolsa,c.Bolsa, c.BolsaID from bolsas c, tiposBolsa t 
where c.TipoBolsaID = t.TipoBolsaID*/

/*select d.Descripcion, f.Clasificacion, d.Detalle, 
c.Caja, tc.TipoCaja, b.Bolsa, tb.TipoBolsa, d.Cantidad, d.DetalleID 
from detalles d, cajas c, bolsas b, clasificaciones f, TiposCaja tc, tiposBolsa tb 
where d.CajaID = c.CajaID and d.BolsaID = b.BolsaID and b.TipoBolsaID = tb.TipoBolsaID
and d.ClasificacionID = f.ClasificacionID 
and c.TipoCajaID = tc.TipoCajaID 
ORDER BY upper(d.Descripcion) ASC

SELECT CajaID, Caja FROM cajas ORDER BY upper(Caja)

select TipoBolsa from tiposBolsa where TipoBolsaID = 3

select TipoBolsa from tiposBolsa t, bolsas b where b.BolsaID = 9 and t.TipoBolsaID = b.TipoBolsaID

select b.*, t.* from cajas b, tiposCaja t where b.TipoCajaID = t.TipoCajaID

update detalles set detalle = '*' || detalle 

select * from detalles order by DetalleID desc

insert into secciones (Seccion) values ('Electrónica')

update clasificaciones set SeccionID = 1

select t.TipoCaja, s.seccion from tiposCaja t, cajas c, secciones s where c.CajaID = 3 
and t.TipoCajaID = c.TipoCajaID and c.SeccionID = s.SeccionID

select t.TipoBolsa, s.seccion from tiposBolsa t, bolsas c, secciones s where c.BolsaID = 18 
and t.TipoBolsaID = c.TipoBolsaID and c.SeccionID = s.SeccionID

select d.Descripcion, f.Clasificacion, d.Detalle, c.Caja, tc.TipoCaja, b.Bolsa, tb.TipoBolsa, d.Cantidad, d.DetalleID 
from detalles d, cajas c, bolsas b, clasificaciones f, TiposCaja tc, tiposBolsa tb 
where d.CajaID = c.CajaID 
and d.BolsaID = b.BolsaID 
and c.SeccionID = 5 and b.SeccionID = 5 and f.SeccionID = 5
and d.ClasificacionID = f.ClasificacionID 
and c.TipoCajaID = tc.TipoCajaID 
and b.TipoBolsaID = tb.TipoBolsaID 

select * from detalles where ClasificacionID = 9
*/


select dt.DetalleID, dt.Descripcion, dt.Detalle, cj.Caja, bl.Bolsa, cl.Clasificacion, sc.seccion, dt.cantidad
from detalles dt, cajas cj, bolsas bl, clasificaciones cl, secciones sc
where dt.CajaID = cj.CajaID and dt.BolsaID = bl.BolsaID and dt.ClasificacionID = cl.ClasificacionID
and cj.SeccionID = sc.SeccionID and bl.SeccionID = sc.SeccionID and cl.SeccionID = sc.SeccionID
order by sc.SeccionID, cj.CajaID, dt.DetalleID





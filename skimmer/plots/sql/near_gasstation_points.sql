SELECT * FROM (SELECT a.* from
near_gasstation a left join fuelsta b
on a.loc <@> b.loc < 0.01::double precision) as foo
WHERE fuelsta_loc IS NOT NULL;


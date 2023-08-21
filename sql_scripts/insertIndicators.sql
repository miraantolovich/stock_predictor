CREATE PROCEDURE dbo.InsertIndicators
        @param_r_percent nvarchar(30),
        @param_si_k nvarchar(30),
        @param_si_d nvarchar(30)
AS
BEGIN
    -- SET NOCOUNT ON added to prevent extra result sets from
    -- interfering with SELECT statements.
    SET NOCOUNT ON;


    -- Convert params to vars we need, also parameter sniffeing (always use local vars inside not params)
    DECLARE @r_percent AS decimal(18,2);
    DECLARE @si_k AS decimal(18,2);
    DECLARE @si_d AS decimal(18,2);

    -- try cast converts to decimal in this code... But if it fails, like if the value is 'None', it will give a NULL as the value
    SET @r_percent = TRY_CAST(REPLACE( @param_r_percent, ',', '') AS decimal(18, 2))
    SET @si_k = TRY_CAST(REPLACE( @param_si_k, ',', '') AS decimal(18, 2))
    SET @si_d = TRY_CAST(REPLACE( @param_si_d, ',', '') AS decimal(18, 2))

    -- Insert statements for procedure here
    INSERT INTO dbo.Indicators( r_percent, si_k, si_d ) VALUES ( @r_percent, @si_k, @si_d ); 

END

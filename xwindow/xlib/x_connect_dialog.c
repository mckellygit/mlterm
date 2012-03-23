/*
 *	$Id$
 *
 *	Note that protocols except ssh aren't supported if USE_LIBSSH2 is defined.
 */

#ifdef  USE_LIBSSH2


#include  "../x_connect_dialog.h"

#include  <stdio.h>		/* sprintf */
#include  <kiklib/kik_mem.h>	/* alloca */
#include  <kiklib/kik_str.h>	/* strdup */
#include  <kiklib/kik_debug.h>
#include  <kiklib/kik_def.h>	/* USE_WIN32API */
#include  <ctype.h>
#include  <kiklib/kik_util.h>
#include  <ml_pty.h>


#define  LINESPACE   10
#define  BEGENDSPACE  8

#define  CLEAR_DRAW   1
#define  DRAW         2
#define  DRAW_EXPOSE  3


/* --- global functions --- */

int
x_connect_dialog(
	char **  uri ,		/* Should be free'ed by those who call this. */
	char **  pass ,		/* Same as above. If pass is not input, "" is set. */
	char *  display_name ,
	Window  parent_window ,
	char **  sv_list ,
	char *  def_server	/* (<user>@)(<proto>:)<server address>(:<encoding>). */
	)
{
	Display *  display ;
	int  screen ;
	Window  window ;
	GC  gc ;
	XFontStruct *  font ;
	u_int  width ;
	u_int  height ;
	u_int  ncolumns ;
	char *  title ;
	size_t  pass_len ;

	if( ! ( title = alloca( (ncolumns = 20 + strlen( def_server)))))
	{
		return  0 ;
	}
	sprintf( title , "Enter password for %s" , def_server) ;
	
	if( ! ( display = XOpenDisplay( display_name)))
	{
		return  0 ;
	}

	screen = DefaultScreen( display) ;
	gc = DefaultGC( display , screen) ;

	if( ! ( font = XLoadQueryFont( display , "-*-r-normal--*-*-*-*-c-*-iso8859-1")))
	{
		XCloseDisplay( display) ;

		return  0 ;
	}

	XSetFont( display , gc , font->fid) ;

	width = font->max_bounds.width * ncolumns + BEGENDSPACE ;
	height = (font->ascent + font->descent + LINESPACE) * 2 ;

	if( ! ( window = XCreateSimpleWindow( display ,
				DefaultRootWindow( display) ,
				(DisplayWidth( display , screen) - width) / 2 ,
				(DisplayHeight( display , screen) - height) / 2 ,
				width , height , 0 ,
				BlackPixel( display , screen) , WhitePixel( display , screen))))
	{
		XFreeFont( display , font) ;
		XCloseDisplay( display) ;

		return  0 ;
	}

	XStoreName( display , window , title) ;
	XSetIconName( display , window , title) ;
	XSelectInput( display , window , KeyReleaseMask|ExposureMask|StructureNotifyMask) ;
	XMapWindow( display , window) ;

	*pass = strdup( "") ;
	pass_len = 1 ;

	while( 1)
	{
		XEvent  ev ;
		int  redraw = 0 ;

		XWindowEvent( display , window ,
			KeyReleaseMask|ExposureMask|StructureNotifyMask , &ev) ;

		if( ev.type == KeyRelease)
		{
			char  buf[10] ;
			void *  p ;
			size_t  len ;

			if( ( len = XLookupString( &ev.xkey , buf , sizeof(buf) ,
							NULL , NULL)) > 0)
			{
				if( buf[0] == 0x08)	/* Backspace */
				{
					if( pass_len > 1)
					{
						(*pass)[--pass_len] = '\0' ;
						redraw = CLEAR_DRAW ;
					}
				}
				else if( isprint( (int)buf[0]))
				{
					if( ! ( p = realloc( *pass , (pass_len += len))))
					{
						break ;
					}

					memcpy( (*pass = p) + pass_len - len - 1 , buf , len) ;
					(*pass)[pass_len - 1] = '\0' ;

					redraw = DRAW ;
				}
				else
				{
					/* Exit loop */
					break ;
				}
			}
		}
		else if( ev.type == Expose)
		{
			redraw = DRAW_EXPOSE ;
		}
		else if( ev.type == MapNotify)
		{
			XSetInputFocus( display , window , RevertToPointerRoot , CurrentTime) ;
		}

		if( redraw)
		{
			XPoint  points[5] =
			{
				{ BEGENDSPACE / 2 , font->ascent + font->descent + LINESPACE } ,
				{ width - BEGENDSPACE / 2 ,
					font->ascent + font->descent + LINESPACE } ,
				{ width - BEGENDSPACE / 2 ,
					(font->ascent + font->descent) * 2 + LINESPACE * 3 / 2} ,
				{ BEGENDSPACE / 2 ,
					(font->ascent + font->descent) * 2 + LINESPACE * 3 / 2} ,
				{ BEGENDSPACE / 2 ,
					font->ascent + font->descent + LINESPACE } ,
			} ;

			if( redraw == DRAW_EXPOSE)
			{
				XDrawString( display , window , gc ,
					BEGENDSPACE / 2 , font->ascent + LINESPACE / 2 ,
					title , strlen(title)) ;

				XDrawLines( display , window , gc , points , 5 , CoordModeOrigin) ;
			}
			else  if( redraw == CLEAR_DRAW)
			{
				XClearArea( display , window , points[0].x + 1 , points[0].y + 1 ,
					points[2].x - points[0].x - 1 ,
					points[2].y - points[0].y - 1 , False) ;
			}
			
			if( *pass)
			{
				char *  input ;
				size_t  count ;

				if( ! ( input = alloca( pass_len - 1)))
				{
					break ;
				}

				for( count = 0 ; count < pass_len - 1 ; count++)
				{
					input[count] = '*' ;
				}

				XDrawString( display , window , gc ,
					BEGENDSPACE / 2 + font->max_bounds.width / 2 ,
					font->ascent * 2 + font->descent + LINESPACE * 3 / 2 ,
					input , K_MIN(pass_len - 1,ncolumns - 1)) ;
			}
		}
	}

	XDestroyWindow( display , window) ;
	XFreeFont( display , font) ;
	XCloseDisplay( display) ;

	*uri = strdup( def_server) ;

#ifdef  DEBUG
	kik_debug_printf( KIK_DEBUG_TAG " Connecting to %s %s\n" , *uri , *pass) ;
#endif

	return  1 ;
}


#endif
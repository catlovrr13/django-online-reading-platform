// components
// import GridMotion from "@/components/GridMotion";
import { Button } from "@/components/ui/button";
import ScrollFloat from "@/components/ScrollFloat";
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from "@/components/ui/carousel";
import { Card, CardContent } from "@/components/ui/card";
import { Header1, Header2, Header3 } from "@/components/custom-components/headers";

// media
import dDark from "@/assets/media/hero-d-dark.svg"
import dLight from "@/assets/media/hero-d-light.svg"
import mDark from "@/assets/media/hero-m-dark.svg"
import mLight from "@/assets/media/hero-m-light.svg"

// function
import { useTheme } from "@/components/theme-provider";
import Autoplay from "embla-carousel-autoplay"

export const iframeHeight = "800px";

export default function Page() {
  const { theme } = useTheme();
  const heroBG =
    theme === "dark" ? `bg-stone-900 opacity-40` : `bg-stone-200 opacity-40`;
  const cardAd =
    theme === "dark" ? `bg-stone-100 opacity-10` : `bg-stone-900 opacity-20`;
  const heroImage = theme === 'dark'
    ? <img src={mDark} alt="hero mobile dark" className="md:hidden rotate-90 w-full h-full object-cover rounded-r-[100px]" />
    : <img src={mLight} alt="hero mobile light" className="md:hidden rotate-90 w-full h-full object-cover rounded-r-[100px]" />;
  const heroImageDesktop = theme === 'dark' ? dDark : dLight;

  return (
    <>
      <div className="flex flex-col gap-0 justify-center">
        {/* hero section */}
          <div className="relative flex overflow-hidden rounded-b-[100px] mb-10 drop-shadow-lg dark:drop-shadow-stone-900 dark:drop-shadow-xl min-h-[400px] min-w-[400px]">
            {/* content */}
            <div className="absolute z-10 flex flex-col md:flex-row p-10 gap-5 justify-evenly w-full h-full">
              <div className="flex-1 flex-col flex gap-5">
                <Header1 text={"theonyxpub."} cl={'text-3xl md:text-5xl'}/>
                <Header2 text={"this is an online reading platform haha"} cl={'font-light'}/>
              </div>
              <div className="flex-1 content-end">
                <Header3 text={"heh"} />
              </div>
            </div>
            {/* background */}
            <div className="relative w-full h-full md:h-full md:w-full aspect-square md:aspect-auto object-cover rounded-b-[100px]">
              <div className="md:hidden w-full h-full flex items-center justify-center rounded-b-[100px]">
                {heroImage}
              </div>
              <img
                src={heroImageDesktop}
                alt="hero"
                className="hidden md:block w-full h-full object-cover rounded-b-[100px] min-h-[300px] min-w-[300px]"
              />
            </div>
          </div>


        {/* genre */}
        <div
          className={`overflow-hidden w-full  flex flex-col gap-5 p-5 justify-center items-center`}
        >
          <ScrollFloat
            animationDuration={3}
            ease="back.inOut(2)"
            scrollStart="center bottom+=50%"
            scrollEnd="bottom bottom-=40%"
            stagger={0.04}
            
          >
            Genres
          </ScrollFloat>
          <Carousel
            opts={{
              align: "start",
            }}
            plugins={[
              Autoplay({
                delay: 2000,
              }),
            ]}
            className="w-full max-w-[20rem] sm:max-w-xs md:max-w-sm "
          >
            <CarouselContent>
              {Array.from({ length: 5 }).map((_, index) => (
                <CarouselItem key={index} className="basis-1/2 lg:basis-1/3">
                  <div className="p-1">
                    <Card>
                      <CardContent className="flex aspect-square items-center justify-center p-6">
                        <span className="text-3xl font-semibold">
                          {index + 1}
                        </span>
                      </CardContent>
                    </Card>
                  </div>
                </CarouselItem>
              ))}
            </CarouselContent>
            <CarouselPrevious />
            <CarouselNext />
          </Carousel>
        </div>

        {/* subscription ad */}
        <div className={`h-100 ${heroBG} flex flex-col p-10 justify-center`}>
          <div className={`h-50 w-full max-w-3xl mx-auto ${cardAd}`}></div>
        </div>
      </div>
    </>
  );
}
